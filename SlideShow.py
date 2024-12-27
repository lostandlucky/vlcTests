import vlc
import tkinter as tk
from PIL import Image, ImageTk
import time
import os

class SlideShow:
    def __init__(self, viewer, controller, media_folder):
                
        #Reference Viewer
        self.viewer = viewer
        
        #Reference Controller
        self.controller = controller
        self.controller.incrementCallback = self.increment_media_index
        self.controller.decrementCallback = self.decrement_media_index
        self.startCallback = self.display_media
        self.controller.quitCallback = self.stop
        
        self.transitioning = False
        
        #VLC Setup
        # self.instance = vlc.Instance('--input-repeat=999999')
        # self.instance = vlc.Instance( '--avcodec-hw=none','--verbose=2', '--file-logging', '--logfile=vlc.log')
        #self.instance = vlc.Instance('--avcodec-hw=none', '--verbose=2', '--file-logging', '--logfile=vlc.log')

        self.instance = vlc.Instance(
            '--avcodec-hw', 'none',
            '--verbose=2',
            '--file-logging',
            '--logfile=vlc.log'
        )


        self.player = self.instance.media_player_new()
        
        #Media
        self.media_folder = media_folder
        self.media_files = self.load_media_locations(self.media_folder)

        #Controls
        self.current_media_index = 0
    
        #Start the show
        self.display_media()
    
    def increment_media_index(self):
        self.viewer.root.after(0, self.run_increment)
        
    def run_increment(self):
        print("Incrementing") #debugging
        self.current_media_index = (self.current_media_index + 1) % len(self.media_files)
        self.display_media()
        
    def decrement_media_index(self):
        self.viewer.root.after(0, self.run_decrement)
    
    def run_decrement(self):
        #TODO: Possibly make it so that it can't go further back than the beginning
        self.current_media_index = (self.current_media_index - 1) % len(self.media_files)
        self.display_media()
    
    def display_media(self):
        """
        Called to move to the next media (video or image).
        """
        # If we're in the middle of a transition, ignore new calls
        if self.transitioning:
            print("Display request ignored: currently transitioning.")
            return
        
        media_path = self.media_files[self.current_media_index]
        print('displaying:', media_path) #debugging
        if media_path.endswith(('.png', '.jpg', '.jpeg')):
            self.show_image(media_path)
        elif media_path.endswith(('.mp4', '.mkv', '.mov', '.gif')):
            self.play_video(media_path)
    
    def play_video(self, media_path):

        
        self.transitioning = True
        
        delay_ms = 1000
        # self.viewer.root.after(delay_ms, lambda: self._finish_video_transition(media_path))
        
        """
        Actually start playing the next video after the transition delay.
        """
        media = self.instance.media_new(media_path)
        self.player.set_media(media)
        
        self.player.set_xwindow(self.viewer.get_window_id())
        self.viewer.show_video()
        self.player.play()
        
        # End transition
        self.transitioning = False
        
    def _finish_video_transition(self, media_path):
        """
        Actually start playing the next video after the transition delay.
        """
        media = self.instance.media_new(media_path)
        self.player.set_media(media)
        
        self.player.set_xwindow(self.viewer.get_window_id())
        self.viewer.show_video()
        self.player.play()
        
        # End transition
        self.transitioning = False
        
    def show_image(self, media_path):
        self.player.stop()
        
        print('showing image:', media_path) #debugging
        image = Image.open(media_path)
        self.viewer.window.update_idletasks()
        resized_image = self.resize_photo(image)

        photo = ImageTk.PhotoImage(resized_image)
        
        self.viewer.show_image(photo)

    def load_media_locations(self, media_folder):
        media_files = [os.path.join(media_folder, f) for f in os.listdir(media_folder) if f.endswith(('.mp4', '.mkv', '.mov', '.avi', '.png', '.jpg', '.jpeg', '.gif'))]
       
        #sort the files in the folder alphabetically
        media_files.sort()
        if not media_files:
            raise FileNotFoundError(f"No media files found in the folder: {media_folder}")
        return media_files
    
    def stop(self, optional_event=None):
        self.player.stop()
        self.viewer.quit()
        
    def resize_photo(self, image):
        # Get the dimensions of the window
        window_width = self.viewer.window.winfo_width()
        window_height = self.viewer.window.winfo_height()
        
        if window_width < 5 or window_height < 5:
            window_width = 800
            window_height = 600
        
        # Get the dimensions of the image
        image_width, image_height = image.size
        
        # Calculate the aspect ratios
        window_aspect = window_width / window_height
        image_aspect = image_width / image_height
        
        # Determine the scaling factor
        if window_aspect > image_aspect:
            # Window is wider than the image
            scale_factor = window_height / image_height
        else:
            # Window is taller than the image
            scale_factor = window_width / image_width
        
        # Calculate the new dimensions of the image
        new_width = int(image_width * scale_factor)
        new_height = int(image_height * scale_factor)
        
        # Resize the image
        resized_image = image.resize((new_width, new_height))
        return resized_image