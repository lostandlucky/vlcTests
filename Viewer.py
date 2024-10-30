import tkinter as tk

class Viewer:
    def __init__(self):
        # Initialize Tkinter window
        self.root = tk.Tk()
        ##self.root.title("VLC Video Player")
        self.window = self.create_window()
        # self.canvas = tk.Canvas(self.window)
        # self.canvas.pack(fill=tk.BOTH, expand=1)
        self.imageContainer = None
        
        # self.root.lift()
        # self.root.attributes('-topmost', True)
        # self.root.after_idle(self.root.attributes, '-topmost', False)

        # Bind the right arrow key to go to the next video
        # self.root.bind("<Right>", self.increment_media_index)
        # self.root.bind("<Left>", self.decrement_media_index)
        # self.root.bind("<Escape>", self.quit)

        


        # Call the play_first_video function after the window is created
    
    def create_window(self):
        window = tk.Frame(self.root)

        # Set the size of the window to full screen
        self.root.attributes('-fullscreen', True)

        #window = tk.Frame(root, width=800, height=600)
        window.pack(fill=tk.BOTH, expand=1)
        
        return window
    
    def get_window_id(self):
        return self.window.winfo_id()
    
    def show_image(self, image):
        if not self.imageContainer:
            print('creating label') #debugging
            self.imageContainer = tk.Label(self.window, image=image)
        self.imageContainer.config(image=image)
        self.imageContainer.image = image
        self.imageContainer.place(x=0, y=0, relwidth=1, relheight=1)
        
        
    def show_video(self):
        if self.imageContainer:
            print('destroying label') #debugging
            self.imageContainer.destroy()
            self.imageContainer = None
    
    def start(self):
        self.root.mainloop()
    
    def quit(self):
        self.root.quit()