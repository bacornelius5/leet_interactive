# class to represent the bot and it's current state (e.g.received the initial startup message)
class Leet:
    
    def __init__(self):

        # has the user has already prompted bot to submit a new problem entry
        self.new_entry = False

        # has the user entered a problem title
        self.runtime_entry = False

        # has the user already entered a runtime
        self.memory_usage = False
    
    