#!/usr/bin/env python3
import vlc
import serial
import time
import threading
import os
import sys
import signal

###############################################################################
# EncoderController - reads encoder data from /dev/ttyS0, calls increments
###############################################################################
class EncoderController:
    def __init__(self, port='/dev/ttyS0', baud=125000):
        self.ser = serial.Serial(
            port=port,
            baudrate=baud,
            timeout=1.0
        )
        self.incrementCallback = None
        self.decrementCallback = None

        self.tics_per_increment = 4
        self.increment_count = 0

        # Rate-limiting: only trigger a "full increment" every X seconds
        self.min_time_between_increment = 0.1
        self.last_increment_time = time.time()

        # Also skip rapid "clicks"
        self.min_time_between_clicks = 0.01
        self.last_click_time = time.time()

        self._running = False
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def start(self):
        self._running = True
        print("Starting EncoderController...")
        self._thread.start()

    def stop(self):
        print("Stopping EncoderController...")
        if self.player:
            self.player.stop()
        self._running = False

    def _loop(self):
        while self._running:
            data = self.ser.read(4)
            if len(data) == 4:
                self.handle_data(data)
        self.ser.close()
        print("Encoder serial closed.")

    def handle_data(self, data: bytes):
        if data == b'\xff\x00\x00\x01':  # Clockwise
            self.increment()
        elif data == b'\xff\x00\x00\xfe':  # Counterclockwise
            self.decrement()
        else:
            print(f"Unknown data: {data}")

    def increment(self):
        now = time.time()
        print('Incrementing...')
        # Basic click gate
        if (now - self.last_click_time) < self.min_time_between_clicks:
            return
        self.last_click_time = now

        self.increment_count = (self.increment_count + 1) % self.tics_per_increment
        if self.increment_count != 0:
            return

        # Also enforce a min time between "full increments"
        if (now - self.last_increment_time) < self.min_time_between_increment:
            return
        self.last_increment_time = now

        if callable(self.incrementCallback):
            print("Calling incrementCallback.")
            self.incrementCallback()
        else:
            print("incrementCallback is not set.")

    def decrement(self):
        now = time.time()
        # Basic click gate
        if (now - self.last_click_time) < self.min_time_between_clicks:
            return
        self.last_click_time = now

        self.increment_count = (self.increment_count - 1) % self.tics_per_increment
        if self.increment_count != 0:
            return

        # Also enforce a min time between "full increments"
        if (now - self.last_increment_time) < self.min_time_between_increment:
            return
        self.last_increment_time = now
        # If you want time gating for decrement too, you can add it:
        if callable(self.decrementCallback):
            print("Calling decrementCallback.")
            self.decrementCallback()
        else:
            print("decrementCallback is not set.")

    def start_video(self, video_path):
        self.media = self.instance.media_new(video_path)
        self.player.set_media(self.media)
        self.player.set_fullscreen(True)
        self.player.play()


###############################################################################
# SlideShow - single VLC window, always fullscreen, re-used for each media
###############################################################################
class SlideShow:
    """
    A slideshow that uses one VLC MediaPlayer in fullscreen for all media (videos or images).
    """
    def __init__(self, controller, media_folder):
        self.controller = controller
        # Attach callbacks
        self.controller.incrementCallback = self.increment_media_index
        self.controller.decrementCallback = self.decrement_media_index

        # Create VLC instance with compositing options
        self.instance = vlc.Instance('--fullscreen', '--avcodec-hw=none',
                                   '--video-x=0', '--video-y=0',
                                   '--marq-opacity=255',
                                   '--file-logging', '--logfile=vlc.log', '--verbose=2')
        
        # Create two players for cross dissolve
        self.player_a = self.instance.media_player_new()
        self.player_b = self.instance.media_player_new()
        self.current_player = self.player_a
        self.next_player = self.player_b
        
        # Set both players to fullscreen
        self.player_a.set_fullscreen(True)
        self.player_b.set_fullscreen(True)
        
        # Configure marquee for filename display
        self.player_a.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)
        self.player_a.video_set_marquee_int(vlc.VideoMarqueeOption.Size, 24)  # font size
        self.player_a.video_set_marquee_int(vlc.VideoMarqueeOption.Position, 9)  # bottom-left
        self.player_a.video_set_marquee_int(vlc.VideoMarqueeOption.Opacity, 255)
        self.player_a.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 0)  # permanent
        
        self.player_b.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)
        self.player_b.video_set_marquee_int(vlc.VideoMarqueeOption.Size, 24)
        self.player_b.video_set_marquee_int(vlc.VideoMarqueeOption.Position, 8)
        self.player_b.video_set_marquee_int(vlc.VideoMarqueeOption.Opacity, 255)
        self.player_b.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 0)
        
        # Load media paths
        self.media_files = self._load_media(media_folder)
        self.current_index = 0
        self.transitioning = False
        self.media_loaded = False
        
        # Start on the first media
        self.display_media()

    def _load_media(self, folder):
        valid_exts = ('.mp4','.mkv','.mov','.avi',
                      '.png','.jpg','.jpeg','.gif')
        all_files = []
        for f in sorted(os.listdir(folder)):
            if f.lower().endswith(valid_exts):
                all_files.append(os.path.join(folder, f))
        if not all_files:
            raise FileNotFoundError(f"No media found in {folder}")
        return all_files

    def increment_media_index(self):
        if self.transitioning:
            print("Ignoring increment, because we are in a transition.")
            return
        self.current_index = (self.current_index + 1) % len(self.media_files)
        self.display_media()

    def decrement_media_index(self):
        if self.transitioning:
            print("Ignoring decrement, because we are in a transition.")
            return
        self.current_index = (self.current_index - 1) % len(self.media_files)
        self.display_media()

    def display_media(self):
        if self.transitioning:
            print("Another display is in progress, ignoring.")
            return
        
        media_path = self.media_files[self.current_index]
        filename = os.path.basename(media_path)
        print(f"Displaying: {media_path}")
        self.transitioning = True
        self.media_loaded = False

        # Prepare next media on the inactive player
        media = self.instance.media_new(media_path)
        self.next_player.set_media(media)
        self.next_player.audio_set_volume(0)
        
        # if there is a # in the filename
        if '#' in filename:
            artist = filename.split('#')[1].replace('_', ' ')
            self.next_player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, artist)
        else:
            self.next_player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, '')
        
        self.next_player.play()
        
        # Wait for media to be properly loaded
        max_wait = 20  # Maximum wait time in deciseconds
        while max_wait > 0 and not self.next_player.will_play():
            time.sleep(0.1)
            max_wait -= 1
            
        # Additional small delay to ensure media is ready
        time.sleep(0.3)
        
        # Now get dimensions and set marquee
        video_height = self.next_player.video_get_height() or 1080  # fallback to 1080p
        font_size = max(24, int(video_height / 30))  # minimum size of 24
        print(f"Video height: {video_height}, Font size: {font_size}")
        
        self.next_player.video_set_marquee_int(vlc.VideoMarqueeOption.Size, 0)
        self.next_player.video_set_marquee_int(vlc.VideoMarqueeOption.Position, 9)
        
        # Cross fade between players
        steps = 51  # Number of steps for fade
        for i in range(steps):
            # Fade video
            opacity = int((i / (steps-1)) * 255)
            self.next_player.video_set_marquee_int(vlc.VideoMarqueeOption.Opacity, opacity)
            
            # Fade audio
            vol_out = int(100 * (1 - (i / (steps-1))))
            vol_in = int(100 * (i / (steps-1)))
            self.current_player.audio_set_volume(vol_out)
            self.next_player.audio_set_volume(vol_in)
            
            time.sleep(0.02)
        
        # Ensure clean state
        self.current_player.audio_set_volume(0)
        self.current_player.stop()
        self.next_player.audio_set_volume(100)
        
        # Swap players
        self.current_player, self.next_player = self.next_player, self.current_player
        
        self.transitioning = False

    def stop(self):
        print("Slideshow stopping.")
        self.player_a.stop()
        self.player_b.stop()


###############################################################################
# Main script
###############################################################################
def main(media_folder='Videos', serial_port='/dev/ttyS0'):
    # 1) Create the EncoderController
    controller = EncoderController(port=serial_port)
    # 2) Create the slideshow
    slideshow = SlideShow(controller, media_folder)
    # 3) Start reading encoder
    controller.start()

    # Graceful shutdown on Ctrl+C
    def signal_handler(sig, frame):
        print("Caught Ctrl+C, exiting...")
        controller.stop()
        slideshow.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print("Slideshow running. Press Ctrl+C to exit.")
    while True:
        time.sleep(1)

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else 'Videos'
    port = sys.argv[2] if len(sys.argv) > 2 else '/dev/ttyS0'
    main(folder, port)
