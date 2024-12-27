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
    def __init__(self, port='/dev/ttyUSB0', baud=9600):
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

        # Add VLC initialization
        self.instance = vlc.Instance('--fullscreen')
        self.player = self.instance.media_player_new()
        self.media = None

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

        # Create a single VLC instance + media player
        # Pass in --avcodec-hw=none if you want to try forcing software decode
        self.instance = vlc.Instance('--fullscreen', '--avcodec-hw=none', '--file-logging',
                                     '--logfile=vlc.log', '--verbose=2', )
        self.player = self.instance.media_player_new()

        # Load media paths
        self.media_files = self._load_media(media_folder)
        self.current_index = 0

        self.transitioning = False
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
        # If already transitioning, skip
        if self.transitioning:
            print("Another display is in progress, ignoring.")
            return
        
        media_path = self.media_files[self.current_index]
        print(f"Displaying: {media_path}")

        # Mark transition
        self.transitioning = True

        # Stop the previous playback if any
        self.player.stop()

        # Tiny delay can sometimes help on Pi
        time.sleep(0.5)

        # Play the new file on the same player
        self.play_media(media_path)

        # End transition
        self.transitioning = False

    def play_media(self, media_path):
        media = self.instance.media_new(media_path)
        self.player.set_media(media)
        
        # Launch the same window in fullscreen
        # We rely on the same MediaPlayer each time -> single window
        self.player.play()

        # Give it a moment to start, then set fullscreen
        time.sleep(0.2)
        self.player.set_fullscreen(True)
        # If you'd like to disable keyboard/mouse input:
        # self.player.video_set_key_input(False)
        # self.player.video_set_mouse_input(False)

    def stop(self):
        print("Slideshow stopping.")
        self.player.stop()


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
