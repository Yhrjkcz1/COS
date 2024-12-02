# src/process.py
import random
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.color = self.generate_color() 
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0
        self.start_time = -1  
        self.response_time = None
    def generate_color(self):
        r = random.randint(180, 255)
        g = random.randint(180, 255)
        b = random.randint(180, 255)
        return f'#{r:02x}{g:02x}{b:02x}'  

    def __repr__(self):
        return (f"Process {self.pid}: Arrival={self.arrival_time}, Burst={self.burst_time}, "
                f"Priority={self.priority}")
    def calculate_response_time(self):
        if self.start_time is not None:
            self.response_time = self.start_time - self.arrival_time
    def reset_state(self):
        """Reset the process metrics before running a new scheduling algorithm"""
        self.remaining_time = self.burst_time
        self.start_time = -1
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = None
