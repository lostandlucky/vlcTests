import vlc
import time

instance = vlc.Instance('--no-audio', '--fullscreen')
player = instance.media_player_new()
media = instance.media_new('Videos/CarMovie1.mov')
player.set_media(media)
player.play()
time.sleep(10)