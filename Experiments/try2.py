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
        self.media_files = [f for f in os.listdir(media_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mkv'))]
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

        self.show_media()
        self.cycle_media()

    def show_media(self):
        media_path = os.path.join(self.media_folder, self.media_files[self.media_index])

        # Check if it's an image or video
        if media_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            self.show_image(media_path)
        elif media_path.endswith(('.mp4', '.mkv', '.mov')):
            print('Playing video:', media_path)
            self.show_video(media_path)

    def show_image(self, image_path):
        print('Showing image:', image_path)
        if self.current_media_is_video:
            # Stop video if it was playing
            self.player.stop()
            self.current_media_is_video = False

        image = Image.open(image_path)
        image = image.resize((800, 600))  # Resize to fit the window
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo  # Keep a reference to avoid garbage collection

    def show_video(self, video_path):
        print('Playing video:', video_path)
        if self.current_media_is_video:
            self.player.stop()  # Stop any previous video playing

        self.current_media_is_video = True
        media = self.instance.media_new(video_path)
        self.player.set_media(media)

        # Get the handle of the tkinter window to display the video
        self.player.set_xwindow(self.label.winfo_id())

        # Play the video
        self.player.play()

        # Stop the video after the specified duration (5 seconds)
        self.after(self.video_duration, self.stop_video)

    def stop_video(self):
        # Stop the video and move to the next media
        print('Stopping video')
        if self.current_media_is_video:
            self.player.stop()
            self.current_media_is_video = False
        self.cycle_media()

    def cycle_media(self):
        self.media_index = (self.media_index + 1) % len(self.media_files)  # Loop through the media
        if not self.current_media_is_video:  # If it's an image, use the delay
            self.after(self.delay, self.show_media)
        else:
            self.show_media()

if __name__ == "__main__":
    folder_path = "Videos"  # Replace with the path to your media folder
    app = MediaSlideshow(folder_path, delay=3000, video_duration=5000)  # Delay is in milliseconds for images, 5 seconds for videos
    app.mainloop()