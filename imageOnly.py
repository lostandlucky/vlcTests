import os
import tkinter as tk
from PIL import Image, ImageTk

class ImageSlideshow(tk.Tk):
    def __init__(self, image_folder, delay=3000):
        super().__init__()

        self.image_folder = image_folder
        self.delay = delay  # Time between images in milliseconds
        self.image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        self.image_files.sort()  # Optionally sort the files alphabetically
        self.image_index = 0

        if not self.image_files:
            print("No images found in the folder")
            self.quit()

        # Set up the label to display the images
        self.label = tk.Label(self)
        self.label.pack()

        self.show_image()
        self.cycle_images()

    def show_image(self):
        # Load the image and update the label
        image_path = os.path.join(self.image_folder, self.image_files[self.image_index])
        image = Image.open(image_path)
        image = image.resize((800, 600))  # Resize to fit the window
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo  # Keep a reference to avoid garbage collection

    def cycle_images(self):
        self.image_index = (self.image_index + 1) % len(self.image_files)  # Loop through the images
        self.show_image()
        self.after(self.delay, self.cycle_images)

if __name__ == "__main__":
    folder_path = "Videos"  # Replace with the path to your image folder
    app = ImageSlideshow(folder_path, delay=3000)  # Delay is in milliseconds
    app.mainloop()
