import time
import threading
import serial


class EncoderController:
    
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=125000,
            timeout=1.0  # 1-second timeout
        )
        self.incrementCallback = None
        self.decrementCallback = None
        self.tics_per_increment = 3
        self.last_increment_time = time.time()
        self.min_time_between_increment = 5
        
        self.last_click_time = time.time()
        self.min_time_between_clicks = 0.2
        self.increment_count = 0
        self.t1 = threading.Thread(target=self.begin_loop)
    
    def checkIncrementTimes(self, now):
        if (time.time() - self.last_click_time) < self.min_time_between_clicks:
            return False
        
        self.increment_count = (self.increment_count + 1) % self.tics_per_increment
        self.last_click_time = now
        
        # Check if it's reached ticks_per_increment
        if (self.increment_count) != 0:
            return False
        
        # Check if it's been long enough since the last increment
        if (time.time() - self.last_increment_time) < self.min_time_between_increment:
            return False
        
        self.last_increment_time = now
        return True

    
    def increment(self):
        now = time.time()
        
        if self.checkIncrementTimes(now):
            # Check if incrementCallback is not a function
            if not callable(self.incrementCallback):
                #throw an error
                #TODO: Implement a better error handling mechanism
                print("Error: incrementCallback is not a function.")
            else:
                print("Calling incrementCallback.")
                self.incrementCallback()
    
    def decrement(self):
        now = time.time()
        
        if self.checkIncrementTimes(now):
        # self.increment_count = (self.increment_count - 1) % self.tics_per_increment
        # print("Default decrement logic.")
        
            if not callable(self.decrementCallback):
                print("Error: decrementCallback is not a function.")
            else:
                if (self.increment_count) == 0:
                    print("Calling decrementCallback.")
                    self.decrementCallback()
        
    def start_controller(self):
        self._running = True
        print("Starting controller...")
        self.t1.start()
        
    def stop_controller(self):
        print("Stopping controller...")
        self._running = False
        # Add conditional statement to check for a vaiable that will stop the loop in begin_loop()
        
    def begin_loop(self):
        
        while self._running:
            # time.sleep(0.2)
            
            data = None
            
            data = self.ser.read(4)
            print(f"Raw data: {data}")
            self.handle_data(data)

        self.ser.close()
            
    def handle_data(self, data):
        # logic for interpreting data
        if data == b'\xff\x00\x00\x01':
            #print("Encoder spinning clockwise")
            self.increment()
        elif data == b'\xff\x00\x00\xfe':
            #print("Encoder spinning counterclockwise")
            self.decrement()
        else:
            print("Unknown state")

        
if __name__ == "__main__":
    controller = EncoderController()
    #controller.start_controller()
    controller.begin_loop()
    #controller.stop_controller()
    print("Exiting...")