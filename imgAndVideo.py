import vlc
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import time

# Create a function to play the initial video
def play_first_video():
    global player  # Make player global to reuse it
    instance = vlc.Instance()
    player = instance.media_player_new()

    # Load the first media file
    media = instance.media_new("Videos/2CarMovie1.mov")
    player.set_media(media)

    # Set the window ID for the player (Tkinter window)
    player.set_xwindow(window.winfo_id())

    # Play the first video
    player.play()

    # Wait 5 seconds, then display image
    root.after(5000, show_image_between_videos)

# Function to show image using OpenCV for 5 seconds between videos
def show_image_between_videos():
    global player
    player.stop()  # Stop the first video

    # Load and display an image using OpenCV
    image = cv2.imread('Videos/1exampleImg.jpg')  # Replace with your actual image path
    height, width, no_channels = image.shape

    # Resize the image to fit the window
    resized_image = cv2.resize(image, (window.winfo_width(), window.winfo_height()))

    # Convert image to RGB (Tkinter-compatible format)
    img_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)

    # Create a label widget to display the image
    label = tk.Label(window, image=img_tk)
    label.image = img_tk  # Keep a reference to avoid garbage collection
    label.place(x=0, y=0, relwidth=1, relheight=1)

    # Wait 5 seconds, then play the second video
    root.after(5000, play_second_video)

# Create a function to play the second video
def play_second_video():
    global player

    # Remove the image label
    for widget in window.winfo_children():
        widget.destroy()

    # Load the second media file
    media = player.get_instance().media_new("Videos/4CNCmovie1.mov")
    player.set_media(media)

    # Ensure the GUI is updated
    window.update_idletasks()
    window.update()

    # Introduce a slight delay to ensure the media is ready
    time.sleep(0.1)

    # Start playback
    player.play()

# Initialize Tkinter window
root = tk.Tk()
root.title("VLC Video Player")

# Set the size of the window
window = tk.Frame(root, width=800, height=600)
window.pack(fill=tk.BOTH, expand=1)

# Set full opacity initially
fade_alpha = 1.0
root.attributes('-alpha', fade_alpha)

# Call the play_first_video function after the window is created
root.after(1000, play_first_video)

# Start the Tkinter main loop
root.mainloop()
