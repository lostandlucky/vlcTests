import vlc
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import time
import os

class SlideShow:
    def __init__(self, viewer, controller, media_folder):
                
        # Reference Viewer
        self.viewer = viewer
        self.canvas = tk.Canvas(self.viewer, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=1)
        
        # Reference Controller
        self.controller = controller
        self.controller.incrementCallback = self.increment_media_index
        self.controller.decrementCallback = self.decrement_media_index
        self.controller.quitCallback = self.stop
        
        # VLC Setup
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.player.set_playback_mode(vlc.PlaybackMode.loop)
        
        # Media
        self.media_folder = media_folder
        self.media_files = self.load_media_locations(self.media_folder)
        
        # Controls
        self.current_media_index = 0
        self.current_media_is_video = False
        
        print(self.media_files) # debugging
        # Start the show
        self.display_media()
    
    def increment_media_index(self):
        print("Incrementing") # debugging
        self.current_media_index = (self.current_media_index + 1) % len(self.media_files)
        self.display_media()
        
    def decrement_media_index(self):
        # TODO: Possibly make it so that it can't go further back than the beginning
        self.current_media_index = (self.current_media_index - 1) % len(self.media_files)
        self.display_media()
    
    def display_media(self):
        media_path = self.media_files[self.current_media_index]
        if media_path.endswith(('.png', '.jpg', '.jpeg')):
            self.show_image(media_path)
        elif media_path.endswith(('.mp4', '.mkv', '.mov', '.gif')):
            self.play_video(media_path)
    
    def play_video(self, media_path):
        self.viewer.show_video()
        
        media = self.instance.media_new(media_path)
        self.player.set_media(media)
        
        self.player.set_xwindow(self.viewer.get_window_id())
        
        # Perform cross dissolve transition
        self.cross_dissolve_video()
        
        self.player.play()
        
    def show_image(self, media_path):
        self.player.stop()
        
        print('showing image:', media_path) # debugging
        image = Image.open(media_path)
        resized_image = self.resize_photo(image)
        photo = ImageTk.PhotoImage(resized_image)
        
        self.cross_dissolve(photo)
    
    def resize_photo(self, image):
        # Get the dimensions of the window
        window_width = self.viewer.winfo_width()
        window_height = self.viewer.winfo_height()
        
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
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        
        return resized_image
    
    def cross_dissolve(self, new_image):
        # Create a blank black image
        width = self.viewer.winfo_width()
        height = self.viewer.winfo_height()
        blank_image = Image.new('RGB', (width, height), 'black')
        blank_photo = ImageTk.PhotoImage(blank_image)
        
        # Get the current image on the canvas
        current_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=blank_photo)
        
        # Perform the cross dissolve transition
        for i in range(0, 101, 5):
            alpha = i / 100.0
            blended_image = Image.blend(blank_image, new_image, alpha)
            blended_photo = ImageTk.PhotoImage(blended_image)
            self.canvas.itemconfig(current_image, image=blended_photo)
            self.canvas.update()
            time.sleep(0.05)
        
        # Set the final image
        self.canvas.itemconfig(current_image, image=new_image)
        self.canvas.image = new_image
    
    def cross_dissolve_video(self):
        # Create a black overlay canvas
        overlay = tk.Canvas(self.viewer, bg='black', width=self.viewer.winfo_width(), height=self.viewer.winfo_height())
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Perform the cross dissolve transition
        for i in range(100, -1, -5):
            alpha = i / 100.0
            overlay.configure(bg=f'#{int(alpha * 255):02x}{int(alpha * 255):02x}{int(alpha * 255):02x}')
            self.viewer.update()
            time.sleep(0.05)
        
        # Remove the overlay
        overlay.destroy()
    
    def stop(self):
        self.player.stop()