import time
import keyboard
import threading

class KeyboardController:
    
    def __init__(self):
        
        # self.connect()
        self.t1 = threading.Thread(target=self.begin_loop)
        
        #self.t1.daemon = True
        # self.begin_loop()
    
    def connect(self):
        print("Default connection logic.")
    
    def increment(self):
        print("Default increment logic.")
        # Check if incrementCallback is not a function
        if not callable(self.incrementCallback):
            #throw an error
            #TODO: Implement a better error handling mechanism
            print("Error: incrementCallback is not a function.")
        else:
            print("Calling incrementCallback.")
            self.incrementCallback()
    
    def decrement(self):
        print("Default decrement logic.")
        
        if not callable(self.decrementCallback):
            print("Error: decrementCallback is not a function.")
        else:
            print("Calling decrementCallback.")
            self.decrementCallback()
        
    def poll_contorller(self):
        print("Default poll logic.")
        
        print("Press 'q' to quit.")
        
    def start_controller(self):
        print("Starting controller...")
        self.t1.start()
        
    def stop_controller(self):
        print("Stopping controller...")
        self.t1.join()
        # Add conditional statement to check for a vaiable that will stop the loop in begin_loop()
        
    def begin_loop(self):
        while True:
            time.sleep(0.1)
            if keyboard.is_pressed('right'):  # Detect if 'right' key is pressed
                print("You pressed 'right'.")
                self.increment()
                
            if keyboard.is_pressed('left'):  # Detect if 'left' key is pressed
                print("You pressed 'left'.")
                self.decrement()
                
            if keyboard.is_pressed('s'):  # Detect if 's' key is pressed
                print("You pressed 's'.")
            
            if keyboard.is_pressed('q'):  # Detect if 'q' key is pressed
                print("You pressed 'q'. Exiting...")
                self.quitCallback()
                break
        #self.stop_controller()
        
        
if __name__ == "__main__":
    controller = KeyboardController()
    #controller.start_controller()
    controller.begin_loop()
    #controller.stop_controller()
    print("Exiting...")