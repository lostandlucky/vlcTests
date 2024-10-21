import vlc
import tkinter as tk

# Create a function to play the initial video
def play_first_video():
    global player  # Make player global to reuse it
    instance = vlc.Instance()
    player = instance.media_player_new()

    # Load the first media file
    media = instance.media_new("Videos/CarMovie1.mov")
    player.set_media(media)

    # Set the window ID for the player (Tkinter window)
    player.set_xwindow(window.winfo_id())

    # Play the first video
    player.play()

    # Wait 5 seconds, then play the second video with fade-in effect
    root.after(5000, play_second_video_with_fade_in)

# Create a function to play the second video
def play_second_video_with_fade_in():
    global fade_alpha
    fade_alpha = 0.0  # Initial opacity for fade-in
    root.attributes('-alpha', fade_alpha)  # Set window transparency to 0 (invisible)

    # Load the second media file
    media = player.get_instance().media_new("Videos/CNCmovie1.mov")
    player.set_media(media)

    # Play the second video
    player.play()

    # Start the fade-in effect
    fade_in()

# Function to perform the fade-in effect
def fade_in():
    global fade_alpha
    if fade_alpha < 1.0:
        fade_alpha += 0.05  # Incrementally increase opacity
        root.attributes('-alpha', fade_alpha)  # Apply the new opacity
        root.after(100, fade_in)  # Continue the fade every 100ms
    else:
        root.attributes('-alpha', 1.0)  # Ensure full opacity

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
