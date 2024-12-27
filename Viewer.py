import tkinter as tk

class Viewer:
    def __init__(self):
        # Initialize Tkinter window
        self.root = tk.Tk()
        ##self.root.title("VLC Video Player")
        self.window = self.create_window()
        self.imageContainer = None
    
    def create_window(self):

        window = tk.Frame(self.root)
        
        # set window background color to black
        window.configure(bg='black')

        # Ensure the window is initialized and has default dimensions
        # self.root.geometry("800x600")

        # Set the size of the window to full screen
        self.root.wm_attributes('-type', 'normal')
        self.root.attributes('-fullscreen', True)

        #window = tk.Frame(root, width=800, height=600)
        window.pack(fill=tk.BOTH, expand=1)
        
        return window
    
    def get_window_id(self):
        return self.window.winfo_id()
    
    def show_image(self, image):
        if not self.imageContainer:
            print('creating label') #debugging
            self.imageContainer = tk.Label(self.window, image=image, bg='black')
        self.imageContainer.config(image=image)
        self.imageContainer.image = image

        self.imageContainer.place(x=0, y=0, relwidth=1, relheight=1)
        
        
    def show_video(self):
        if self.imageContainer:
            print('destroying label') #debugging
            self.imageContainer.destroy()
            self.imageContainer = None
    
    def start(self, startCallback=None):
        if callable(startCallback):
            self.root.after(1, startCallback)
        self.root.mainloop()
    
    def quit(self):
        self.root.quit()