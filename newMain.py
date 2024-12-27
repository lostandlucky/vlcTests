#!/usr/bin/env python3

import vlc
import serial
import time
import threading
import os
import sys
import signal

###############################################################################
# Encoder Controller
###############################################################################
class EncoderController:
    """
    Continuously reads 4 bytes from /dev/ttyS0 and interprets them.
    If it sees b'\\xff\\x00\\x00\\x01', it calls incrementCallback()
    If it sees b'\\xff\\x00\\x00\\xfe', it calls decrementCallback().
    """
    def __init__(self, port='/dev/ttyS0', baud=125000):
        self.ser = serial.Serial(
            port=port,
            baudrate=baud,
            timeout=1.0
        )
        self.incrementCallback = None
        self.decrementCallback = None

        self.tics_per_increment = 3
        self.increment_count = 0

        # Time gating to avoid spamming transitions
        self.last_increment_time = time.time()
        self.min_time_between_increment = 5
        
        # For rapid knob spins
        self.last_click_time = time.time()
        self.min_time_between_clicks = 0.2
        
        self._running = False
        self.thread = threading.Thread(target=self.begin_loop, daemon=True)

    def start(self):
        self._running = True
        print("Starting EncoderController...")
        self.thread.start()

    def stop(self):
        print("Stopping EncoderController...")
        self._running = False

    def begin_loop(self):
        while self._running:
            data = self.ser.read(4)
            if len(data) == 4:
                self.handle_data(data)
        self.ser.close()
        print("Encoder serial closed.")

    def handle_data(self, data: bytes):
        # Example: spin clockwise
        if data == b'\xff\x00\x00\x01':
            self.increment()
        # Example: spin counterclockwise
        elif data == b'\xff\x00\x00\xfe':
            self.decrement()
        else:
            print(f"Unknown data: {data}")

    def increment(self):
        now = time.time()

        # Basic rate-limit for "clicks"
        if (now - self.last_click_time) < self.min_time_between_clicks:
            return
        self.last_click_time = now

        # Simple "tics" logic
        self.increment_count = (self.increment_count + 1) % self.tics_per_increment
        
        if self.increment_count != 0:
            return

        # Also limit full "increment" calls
        if (now - self.last_increment_time) < self.min_time_between_increment:
            return
        self.last_increment_time = now

        if callable(self.incrementCallback):
            print("Calling incrementCallback.")
            self.incrementCallback()
        else:
            print("incrementCallback not set.")

    def decrement(self):
        # If you want a separate gating for decrement, implement similarly
        if callable(self.decrementCallback):
            print("Calling decrementCallback.")
            self.decrementCallback()
        else:
            print("decrementCallback not set.")


###############################################################################
# SlideShow (NO TKINTER)
###############################################################################
class SlideShow:
    """
    Minimal slideshow using python-vlc only.

    - If 'play_video()' is called with an image file, VLC can still open it
      but might stop after 10 seconds or so, depending on your VLC version.
    - If it's a video, it plays as usual until you manually skip/stop.
    """
    def __init__(self, controller, media_folder):
        self.controller = controller
        # Set callbacks
        self.controller.incrementCallback = self.increment_media_index
        self.controller.decrementCallback = self.decrement_media_index
        
        # VLC setup
        # (Try forcing software decode if desired)
        self.instance = vlc.Instance('--avcodec-hw=none',
                                     '--file-logging', '--logfile=vlc.log',
                                     '--verbose=2')
        self.player = self.instance.media_player_new()

        self.media_files = self.load_media(media_folder)
        self.current_index = 0
        
        self.transitioning = False

        # Start with the first media
        self.display_media()

    def load_media(self, folder):
        valid_exts = ('.mp4','.mkv','.mov','.avi',
                      '.png','.jpg','.jpeg','.gif')
        all_files = [os.path.join(folder, f) for f in os.listdir(folder)
                     if f.lower().endswith(valid_exts)]
        all_files.sort()
        if not all_files:
            raise FileNotFoundError(f"No media found in {folder}")
        return all_files

    def increment_media_index(self):
        # Called by the encoder thread. Let's just do it inline.
        # If you want to throttle quick increments, add logic here.
        if self.transitioning:
            print("Ignoring increment, transitioning in progress.")
            return
        self.current_index = (self.current_index + 1) % len(self.media_files)
        self.display_media()

    def decrement_media_index(self):
        if self.transitioning:
            print("Ignoring decrement, transitioning in progress.")
            return
        self.current_index = (self.current_index - 1) % len(self.media_files)
        self.display_media()

    def display_media(self):
        if self.transitioning:
            print("Already transitioning, ignoring new request.")
            return
        
        media_path = self.media_files[self.current_index]
        print(f"Displaying: {media_path}")
        
        # You can stop any previous playback
        self.player.stop()

        # Mark that we're in a "transition"
        self.transitioning = True
        time.sleep(0.5)  # optional small delay for stability

        # Actually "play" the new file
        self.play_video(media_path)

        # End transition
        self.transitioning = False

    def play_video(self, media_path):
        media = self.instance.media_new(media_path)
        self.player.set_media(media)

        # If you want fullscreen:
        # self.player.set_fullscreen(True)

        # If you want to embed in a windowless environment, you can skip set_xwindow
        # or if on X11, you can pass an XID. Without tkinter, you might just let VLC
        # open its own window. So just omit set_xwindow() entirely:
        # self.player.set_xwindow(0)

        self.player.play()
        # The video or image is now playing in a separate VLC window.


###############################################################################
# Main
###############################################################################
def main(media_folder='Videos', serial_port='/dev/ttyS0'):
    # Create the controller
    controller = EncoderController(port=serial_port, baud=125000)
    # Create the slideshow
    slideshow = SlideShow(controller, media_folder)

    # Start the controller
    controller.start()

    # Handle Ctrl+C to stop
    def signal_handler(sig, frame):
        print("Ctrl+C pressed, shutting down.")
        controller.stop()
        slideshow.player.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Keep the main thread alive
    print("Running... Press Ctrl+C to stop.")
    while True:
        time.sleep(1)


if __name__ == "__main__":
    # Usage: python this_script.py [media_folder] [serial_port]
    folder = sys.argv[1] if len(sys.argv) > 1 else 'Videos'
    port = sys.argv[2] if len(sys.argv) > 2 else '/dev/ttyS0'
    main(folder, port)
