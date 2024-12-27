from Viewer import Viewer
from EncoderController import EncoderController
from SlideShow import SlideShow
import psutil
import time
import threading
import logging
from datetime import datetime

logging.basicConfig(filename='./app.log', level=logging.DEBUG)

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
logging.debug(f'Starting at {dt_string}')

def monitor_resources():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        logging.debug(f'CPU Usage: {cpu_usage}%')
        logging.debug(f'Memory Usage: {memory_info.percent}%')
        time.sleep(5)

viewer = Viewer()
# resource_thread = threading.Thread(target=monitor_resources)
# resource_thread.start()

controller = EncoderController()

slideShow = SlideShow(viewer, controller, 'Videos')
controller.start_controller()

viewer.start()

# Detect an interupt signal and stop the controller
import signal
import sys
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    controller.stop_controller()
    slideShow.stop()
    sys.exit(0)



# if __name__ == "__main__":
    # play_video('/path/to/your/video.mp4')