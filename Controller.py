class BaseController:
    
    
    
    def __init__(self, root):
        self.root = root
        self.connect()
    
    def connect(self):
        print("Default connection logic.")
    
    def increment(self):
        print("Default increment logic.")
    
    def decrement(self):
        print("Default decrement logic.")
        
    def poll_contorller(self):
        print("Default poll logic.")