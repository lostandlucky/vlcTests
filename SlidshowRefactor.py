import vlc
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import time
import os

class SlideShow:
    def __init__(self, media_folder, run_duration=3000):
        
        # Initialize Tkinter window
        self.root = tk.Tk()
        self.root.title("VLC Video Player")
        
        self.window = tk.Frame(self.root, width=800, height=600)
        self.window.pack(fill=tk.BOTH, expand=1)
        
        #VLC Setup
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        #remove
        self.run_duration = run_duration
        
        #Media
        self.media_folder = media_folder
        self.media_files = self.load_media_locations(self.media_folder)

        #Controls
        self.current_media_index = 0
        self.current_media_is_video = False
        
        # Bind the right arrow key to go to the next video
        self.root.bind("<Right>", self.increment_media_index)
        self.root.bind("<Left>", self.decrement_media_index)
        
        print(self.media_files)
        #Start the show
        
        self.start()
    
    def initialize_tk(self):
        # Initialize Tkinter window
        self.root = tk.Tk()
        self.root.title("VLC Video Player")
        
        self.window = tk.Frame(self.root, width=800, height=600)
        self.window.pack(fill=tk.BOTH, expand=1)
    
    def increment_media_index(self, optional_event):
        print("Incrementing")
        self.current_media_index = (self.current_media_index + 1) % len(self.media_files)
        self.play_video()
        
    def decrement_media_index(self, optional_event):
        #TODO: Possibly make it so that it can't go further back than the beginning
        self.current_media_index = (self.current_media_index - 1) % len(self.media_files)
        self.play_video()
    
    def play_video(self):
        print(self.media_files)
        video_path = self.media_files[self.current_media_index]
        media = self.instance.media_new(video_path)
        self.player.set_media(media)
        
        self.player.set_xwindow(self.window.winfo_id())
        self.player.play()

    def load_media_locations(self, media_folder):
        media_files = [os.path.join(media_folder, f) for f in os.listdir(media_folder) if f.endswith(('.mp4', '.mkv', '.mov'))]
        if not media_files:
            raise FileNotFoundError(f"No media files found in the folder: {media_folder}")
        return media_files
    
    def start(self):
        # Set the size of the window
        

        # slideShow = SlideShow(root, 'Videos')
        # Call the play_first_video function after the window is created
        self.play_video()
        # Start the Tkinter main loop
        self.root.mainloop()