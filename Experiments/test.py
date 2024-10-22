import os
import tkinter as tk
from PIL import Image, ImageTk
import vlc

class MediaSlideshow(tk.Tk):
    def __init__(self, media_folder, delay=3000, video_duration=5000):
        super().__init__()

        self.media_folder = media_folder
        self.delay = delay  # Time between images in milliseconds
        self.video_duration = video_duration  # Video duration in milliseconds (5 seconds)
        self.media_files = [f for f in os.listdir(media_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mkv', '.mov'))]
        self.media_files.sort()  # Optionally sort the files alphabetically
        self.media_index = 0
        self.current_media_is_video = False

        if not self.media_files:
            print("No media found in the folder")
            self.quit()

        # Set up the label to display images
        self.label = tk.Label(self)
        self.label.pack()

        # Set up VLC player for video
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Start with the first media
        self.show_media()
    
    def show_media(self):
        """Shows the current media, whether it's an image or a video."""
        media_path = os.path.join(self.media_folder, self.media_files[self.media_index])

        # Check if it's an image or video
        if media_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            self.show_image(media_path)
        elif media_path.endswith(('.mp4', '.mkv', '.mov')):
            self.show_video(media_path)

    def show_image(self, image_path):
        """Displays an image."""
        if self.current_media_is_video:
            # Stop video if it was playing and reset the flag
            self.player.stop()
            self.current_media_is_video = False

        # Clear the label image in case a video was playing before
        self.label.config(image='')

        # Display image using PIL and tkinter
        image = Image.open(image_path)
        image = image.resize((800, 600), Image.ANTIALIAS)  # Resize to fit the window
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo  # Keep a reference to avoid garbage collection

        # Schedule the next media after the delay
        self.after(self.delay, self.cycle_media)

    def show_video(self, video_path):
        """Plays a video for a fixed duration (5 seconds)."""
        if self.current_media_is_video:
            # Stop any previous video playing
            self.player.stop()

        self.current_media_is_video = True

        # Clear the label image before playing video
        self.label.config(image='')

        # Set up and play the video
        media = self.instance.media_new(video_path)
        self.player.set_media(media)
        self.player.set_xwindow(self.label.winfo_id())
        self.player.play()

        # Stop the video after the specified duration (5 seconds)
        self.after(self.video_duration, self.stop_video)

    def stop_video(self):
        """Stops the video playback and moves to the next media."""
        if self.current_media_is_video:
            self.player.stop()
            self.current_media_is_video = False
        self.cycle_media()

    def cycle_media(self):
        """Moves to the next media and starts the process again."""
        self.media_index = (self.media_index + 1) % len(self.media_files)  # Loop through the media
        self.show_media()

if __name__ == "__main__":
    folder_path = "Videos"  # Replace with the path to your media folder
    app = MediaSlideshow(folder_path, delay=3000, video_duration=5000)  # Delay is in milliseconds for images, 5 seconds for videos
    app.mainloop()
