# class to represent the bot and it's current state (e.g.received the initial startup message)
class Leet:
    
    def __init__(self):

        # dictionary that stores problem data to be added to the mongo collection
        self.problem_data = {}

        # has the user has already prompted bot to submit a new problem entry
        self.new_entry = False

        # has the user already entered the problem title
        self.new_problem = False

        # has the user already entered the runtime
        self.runtime_entry = False

        # has the user already entered a runtime
        self.memory_usage = False

        self.solution = False

        # has the user asked to pull a problem from mongo
        self.should_pull = False


    
    