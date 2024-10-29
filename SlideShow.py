import vlc
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import time
import os

class SlideShow:
    def __init__(self, viewer, controller, media_folder):
        
        #tkinter
        # self.root = root
        
        #Reference Viewer
        self.viewer = viewer
        
        #Reference Controller
        self.controller = controller
        self.controller.incrementCallback = self.increment_media_index
        self.controller.decrementCallback = self.decrement_media_index
        self.controller.quitCallback = self.stop
        
        #VLC Setup
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        #Media
        self.media_folder = media_folder
        self.media_files = self.load_media_locations(self.media_folder)
        # self.label = None

        #Controls
        self.current_media_index = 0
        self.current_media_is_video = False
        
        # Bind the right arrow key to go to the next video
        # self.viewer.root.bind("<Right>", self.increment_media_index)
        # self.viewer.root.bind("<Left>", self.decrement_media_index)
        # self.viewer.root.bind("<Escape>", self.quit)
        
        print(self.media_files) #debugging
        #Start the show
        self.display_media()
    
    def increment_media_index(self):
        print("Incrementing") #debugging
        self.current_media_index = (self.current_media_index + 1) % len(self.media_files)
        self.display_media()
        
    def decrement_media_index(self):
        #TODO: Possibly make it so that it can't go further back than the beginning
        self.current_media_index = (self.current_media_index - 1) % len(self.media_files)
        self.display_media()
    
    def display_media(self):
        media_path = self.media_files[self.current_media_index]
        if media_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            self.show_image(media_path)
        elif media_path.endswith(('.mp4', '.mkv', '.mov')):
            self.play_video(media_path)
    
    def play_video(self, media_path):
        # if self.label:
        #     print('destroying label') #debugging
        #     self.label.destroy()
        #     self.label = None
        self.viewer.show_video()
        
        media = self.instance.media_new(media_path)
        self.player.set_media(media)
        
        # self.player.set_xwindow(window.winfo_id())
        self.player.set_xwindow(self.viewer.get_window_id())
        self.player.play()
        
    def show_image(self, media_path):
        self.player.stop()
        
        print('showing image:', media_path) #debugging
        image = Image.open(media_path)
        image = image.resize((800, 600))
        photo = ImageTk.PhotoImage(image)
        
        self.viewer.show_image(photo)
        
        # if not self.label:
        #     print('creating label') #debugging
        #     self.label = tk.Label(window, image=photo)
        # self.label.config(image=photo)
        # self.label.image = photo
        # self.label.place(x=0, y=0, relwidth=1, relheight=1)
        # self.after(self.delay, self.cycle_media)

    def load_media_locations(self, media_folder):
        media_files = [os.path.join(media_folder, f) for f in os.listdir(media_folder) if f.endswith(('.mp4', '.mkv', '.mov', '.avi', '.png', '.jpg', '.jpeg', '.gif'))]
        if not media_files:
            raise FileNotFoundError(f"No media files found in the folder: {media_folder}")
        return media_files
    
    def stop(self, optional_event=None):
        self.player.stop()
        self.viewer.quit()
        # self.root.quit()
            


if __name__ == "__main__":
    # Initialize Tkinter window
    root = tk.Tk()
    root.title("VLC Video Player")

    # Set the size of the window to full screen
    root.attributes('-fullscreen', True)
    window = tk.Frame(root)
    
    #window = tk.Frame(root, width=800, height=600)
    window.pack(fill=tk.BOTH, expand=1)

    slideShow = SlideShow(root, 'Videos')
    # Call the play_first_video function after the window is created

    # Start the Tkinter main loop
    root.mainloop()