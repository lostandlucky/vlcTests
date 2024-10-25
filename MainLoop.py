from SlideShow import SlideShow
from Viewer import Viewer

viewer = Viewer()

slideShow = SlideShow(viewer, 'Videos')

viewer.start()

# while True:
#     data = ser.read(4)  # Read 4 bytes
#     print(f"Raw data: {data}")
    
#     if data == b'\xff\x00\x00\x01':
#         print("Encoder spinning clockwise")
#         self.switch_vid()
#     elif data == b'\xff\x00\x00\xfe':
#         print("Encoder spinning counterclockwise")
#     else:
#         print("Unknown state")
# ser.close()