# src/scheduler.py

class Scheduler:
    def __init__(self, processes):
        self.processes = processes

    def fcfs(self):
        """First-Come-First-Serve (FCFS) Scheduling"""
        # Sort by arrival time for FCFS scheduling
        self.processes.sort(key=lambda p: p.arrival_time)
        current_time = 0
        for process in self.processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            process.start_time = current_time
            process.waiting_time = current_time - process.arrival_time
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time

    def sjf(self):
        """Shortest Job First (Non-preemptive) Scheduling"""
        current_time = 0
        remaining_processes = sorted(self.processes, key=lambda p: (p.arrival_time, p.burst_time))

        while remaining_processes:
            # Find processes that have arrived and sort them by burst time
            available_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
            if available_processes:
                # Choose process with the shortest burst time
                shortest_process = min(available_processes, key=lambda p: p.burst_time)
                if current_time < shortest_process.arrival_time:
                    current_time = shortest_process.arrival_time
                shortest_process.start_time = current_time
                shortest_process.waiting_time = current_time - shortest_process.arrival_time
                current_time += shortest_process.burst_time
                shortest_process.completion_time = current_time
                shortest_process.turnaround_time = shortest_process.completion_time - shortest_process.arrival_time
                remaining_processes.remove(shortest_process)
            else:
                current_time += 1  # Increment time if no processes are available yet

    def priority_scheduling(self):
        """Priority Scheduling (Non-preemptive)"""
        current_time = 0
        remaining_processes = sorted(self.processes, key=lambda p: (p.arrival_time, p.priority))

        while remaining_processes:
            # Find processes that have arrived and sort by priority
            available_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
            if available_processes:
                # Choose the process with the highest priority (lowest priority number)
                highest_priority_process = min(available_processes, key=lambda p: p.priority)
                if current_time < highest_priority_process.arrival_time:
                    current_time = highest_priority_process.arrival_time
                highest_priority_process.start_time = current_time
                highest_priority_process.waiting_time = current_time - highest_priority_process.arrival_time
                current_time += highest_priority_process.burst_time
                highest_priority_process.completion_time = current_time
                highest_priority_process.turnaround_time = highest_priority_process.completion_time - highest_priority_process.arrival_time
                remaining_processes.remove(highest_priority_process)
            else:
                current_time += 1  # Increment time if no processes are available yet

    def round_robin(self, quantum):
        """Round Robin Scheduling"""
        queue = sorted(self.processes, key=lambda p: p.arrival_time)  # Sort by arrival time initially
        current_time = 0
        while queue:
            for process in list(queue):
                if process.arrival_time <= current_time:
                    # Only start process if it has arrived
                    start_time = max(current_time, process.start_time if process.start_time != -1 else process.arrival_time)
                    # Mark process start time if it hasn't started
                    if process.start_time == -1:
                        process.start_time = start_time
                    # Run process for a time slice (quantum) or until completion
                    time_slice = min(process.remaining_time, quantum)
                    process.remaining_time -= time_slice
                    current_time += time_slice

                    if process.remaining_time == 0:
                        # Process is finished
                        process.completion_time = current_time
                        process.turnaround_time = process.completion_time - process.arrival_time
                        process.waiting_time = process.turnaround_time - process.burst_time
                        queue.remove(process)
                else:
                    # Increment time if no process is ready
                    current_time += 1
