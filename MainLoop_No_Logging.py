# from SlideShow import SlideShow
from Viewer import Viewer
# from KeyboardController import KeyboardController
from EncoderController import EncoderController
from SlideShow import SlideShow

viewer = Viewer()


# controller = KeyboardController()
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

