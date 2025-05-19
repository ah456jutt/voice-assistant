import random
from datetime import datetime
from .system_control import SystemController

class TaskManager:
    def __init__(self):
        self.system_controller = SystemController()
        self.chat_responses = {
            "hello": ["Hello boss!", "Hi there!", "Hey boss!"],
            "how are you": ["I'm doing great boss!", "All systems operational!"],
            "thank you": ["You're welcome boss!", "Anytime!"],
            "i like you": ["i am happy that you liked me!", "Thanks!", "I appreciate it!"],
            "i love you": ["I love you too, boss!", "You're the best!"],
            "default": ["I don't understand that command, boss.", 
                      "Could you try that again?"]
        }

    def handle_command(self, command):
        command = command.lower().strip()
        
        # Handle date and time commands first
        if any(word in command for word in ["time", "clock"]):
            return self.get_time()
        elif any(word in command for word in ["date", "today", "day"]):
            return self.get_date()
            
        # Check for system commands
        base_command = command.split()[0]
        if base_command in self.system_controller.cmd_commands or \
           base_command in self.system_controller.allowed_commands:
            return self.system_controller.execute_basic_command(command)
        
        # Check for other commands
        if "open" in command:
            return self.system_controller.handle_website(command)
            
        if any(word in command for word in ["status", "info", "cpu", "memory"]):
            return self.system_controller.handle_status_command(command)
            
        if command in ["help", "commands", "show commands"]:
            return self.system_controller.show_available_commands()
        
        # Check for chat responses
        for key in self.chat_responses:
            if key in command:
                return random.choice(self.chat_responses[key])
        
        return random.choice(self.chat_responses["default"])

    def get_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        return f"The current time is {current_time}"

    def get_date(self):
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}"