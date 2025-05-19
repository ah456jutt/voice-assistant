import time
from datetime import datetime, timedelta
import random  # Importing random module to use in get_health_tips method

class HealthMonitor:
    def __init__(self):
        self.last_break = datetime.now()
        self.work_duration = timedelta(minutes=45)
        self.break_duration = timedelta(minutes=5)
        
    def check_break_needed(self):
        time_worked = datetime.now() - self.last_break
        if time_worked > self.work_duration:
            return True, f"You've been working for {time_worked.seconds//60} minutes. Time for a break!"
        return False, f"Next break in {(self.work_duration - time_worked).seconds//60} minutes"

    def take_break(self):
        self.last_break = datetime.now()
        return f"Taking a {self.break_duration.seconds//60} minute break. Look away from the screen!"

    def get_health_tips(self):
        tips = [
            "Remember to maintain good posture, boss!",
            "Stay hydrated - drink some water!",
            "Time for some eye exercises - look at something 20 feet away for 20 seconds.",
            "Stand up and stretch for a minute.",
            "Take deep breaths and relax your shoulders."
        ]
        return random.choice(tips)