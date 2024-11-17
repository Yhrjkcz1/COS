class Scheduler:
    def __init__(self, processes):
        self.processes = processes
        self.context_switches = 0  # Initialize context_switches as an instance variable

    def fcfs(self):
        """First-Come-First-Serve (FCFS) Scheduling"""
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
        print("Running SJF Scheduling...")
        current_time = 0
        remaining_processes = sorted(self.processes, key=lambda p: p.arrival_time)

        while remaining_processes:
            available_processes = [p for p in remaining_processes if p.arrival_time <= current_time]

            if available_processes:
                # Select the process with the shortest burst time
                shortest_process = min(available_processes, key=lambda p: p.burst_time)

                if current_time < shortest_process.arrival_time:
                    current_time = shortest_process.arrival_time

                if shortest_process.start_time == -1:  # This means the process hasn't started yet
                    shortest_process.start_time = current_time
                    self.context_switches += 1  # Increment context switch
                    print(f"Process {shortest_process.pid} started at {shortest_process.start_time}")

                shortest_process.waiting_time = current_time - shortest_process.arrival_time
                current_time += shortest_process.burst_time
                shortest_process.completion_time = current_time
                shortest_process.turnaround_time = shortest_process.completion_time - shortest_process.arrival_time

                remaining_processes.remove(shortest_process)
            else:
                current_time += 1  # Increment time if no processes are available yet

    def get_context_switches(self):
        # Ensure context_switches is properly returned
        return self.context_switches
