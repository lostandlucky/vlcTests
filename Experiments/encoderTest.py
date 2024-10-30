import serial
import time

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=125000,
)
    


while True:
    
    # time.sleep(5)
    # ser.reset_input_buffer()
    data = ser.read(4)  # Read 4 bytes
    print(f"Raw data: {data}")
    
    if data == b'\xff\x00\x00\x01':
        print("Encoder spinning clockwise")
    elif data == b'\xff\x00\x00\xfe':
        print("Encoder spinning counterclockwise")
    else:
        print("Unknown state")

ser.close()
