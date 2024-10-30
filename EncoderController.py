import time
import keyboard
import threading
import serial


class EncoderController:
    
    def __init__(self):
        self.ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=125000,
        )
        self.tics_per_increment = 5
        self.increment_count = 0
        self.t1 = threading.Thread(target=self.begin_loop)
    
    def increment(self):
        self.increment_count = (self.increment_count + 1) % self.tics_per_increment
        # print("Default increment logic. {}".format(self.increment_count))
        # print the self.increment_count
        print(f"Default increment logic. {self.increment_count}")
        
        
        # Check if incrementCallback is not a function
        
        
        if not callable(self.incrementCallback):
            #throw an error
            #TODO: Implement a better error handling mechanism
            print("Error: incrementCallback is not a function.")
        else:
            if (self.increment_count) == 0:
                print("Calling incrementCallback.")
                self.incrementCallback()
    
    def decrement(self):
        
        self.increment_count = (self.increment_count - 1) % self.tics_per_increment
        print("Default decrement logic.")
        
        if not callable(self.decrementCallback):
            print("Error: decrementCallback is not a function.")
        else:
            if (self.increment_count) == 0:
                print("Calling decrementCallback.")
                self.decrementCallback()
        
    def start_controller(self):
        print("Starting controller...")
        self.t1.start()
        
    def stop_controller(self):
        print("Stopping controller...")
        # Add conditional statement to check for a vaiable that will stop the loop in begin_loop()
        
    def begin_loop(self):
        
        while True:
            time.sleep(0.1)
            self.ser.reset_input_buffer()
            data = self.ser.read(4)  # Read 4 bytes
            print(f"Raw data: {data}")
            
            if data == b'\xff\x00\x00\x01':
                print("Encoder spinning clockwise")
                self.increment()
            elif data == b'\xff\x00\x00\xfe':
                print("Encoder spinning counterclockwise")
                self.decrement()
            else:
                print("Unknown state")
                
            if keyboard.is_pressed('q'):  # Detect if 'q' key is pressed
                print("You pressed 'q'. Exiting...")
                self.quitCallback()
                break

        self.ser.close()
            
        
        
if __name__ == "__main__":
    controller = EncoderController()
    #controller.start_controller()
    controller.begin_loop()
    #controller.stop_controller()
    print("Exiting...")