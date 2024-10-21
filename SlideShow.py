import vlc
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import time
import os

class SlideShow:
    def __init__(self, root, media_folder, run_duration=3000):
        
        #tkinter
        self.root = root
        
        #VLC Setup
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        #remove
        self.run_duration = run_duration
        
        #Media
        self.media_folder = media_folder
        self.media_files = self.load_media_locations(self.media_folder)
       
        #Start the show
        self.play_video('Videos/1CarMovie1.mov')
    
    def play_video(self, video_path):
        media = self.instance.media_new(video_path)
        self.player.set_media(media)
        self.player.play()
        
        self.player.set_xwindow(window.winfo_id())
        self.player.play()

    def load_media_locations(self, media_folder):
        self.media_files = [f for f in os.listdir(media_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mkv', '.mov'))]



if __name__ == "__main__":
    # Initialize Tkinter window
    root = tk.Tk()
    root.title("VLC Video Player")

    # Set the size of the window
    window = tk.Frame(root, width=800, height=600)
    window.pack(fill=tk.BOTH, expand=1)

    slideShow = SlideShow(root, 'Videos')
    # Call the play_first_video function after the window is created

    # Start the Tkinter main loop
    root.mainloop()