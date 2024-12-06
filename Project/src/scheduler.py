class Scheduler:
    def __init__(self, processes):
        self.processes = processes
        self.context_switches = 0  # Initialize context_switches as an instance variable
        self.execution_log = []  # To store the logs for Gantt chart
        self.response_times = []  # To store response times for each process
        self.queue_lengths = []  # To store the queue length at each time slice

    def fcfs(self):
        """First-Come-First-Serve (FCFS) Scheduling"""
        print("First-Come-First-Serve (FCFS) Scheduling...")
        self.processes.sort(key=lambda p: p.arrival_time)
        current_time = 0
        for process in self.processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            process.start_time = current_time
            process.response_time = process.start_time - process.arrival_time  # Calculate response time
            self.response_times.append(process.response_time)  # Add to response_times
            process.waiting_time = current_time - process.arrival_time
            current_time += process.burst_time
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time

            # Record the process execution for the Gantt chart
            self.execution_log.append({
                "pid": process.pid,
                "start": process.start_time,
                "duration": process.burst_time,
                "color": process.color,
                "response_time": process.response_time,  
                "queue_length": sum(1 for p in self.processes if p.arrival_time <= current_time and p.completion_time is None)
            })

    def sjf_non_preemptive(self):
        """Shortest Job First (Non-preemptive) Scheduling"""
        print("Running SJF (Non-preemptive) Scheduling...")
        current_time = 0
        remaining_processes = sorted(self.processes, key=lambda p: p.arrival_time)

        while remaining_processes:
            available_processes = [p for p in remaining_processes if p.arrival_time <= current_time]

            # Record the queue length
            self.queue_lengths.append(len(available_processes))

            if available_processes:
                # Select the process with the shortest burst time
                shortest_process = min(available_processes, key=lambda p: p.burst_time)

                if current_time < shortest_process.arrival_time:
                    current_time = shortest_process.arrival_time

                if shortest_process.start_time == -1:  # This means the process hasn't started yet
                    shortest_process.start_time = current_time
                    shortest_process.response_time = shortest_process.start_time - shortest_process.arrival_time  # Calculate response time
                    self.response_times.append(shortest_process.response_time)  # Add to response_times
                    # print(f"Process {shortest_process.pid} started at {shortest_process.start_time}")

                shortest_process.waiting_time = current_time - shortest_process.arrival_time
                current_time += shortest_process.burst_time
                shortest_process.completion_time = current_time
                shortest_process.turnaround_time = shortest_process.completion_time - shortest_process.arrival_time
                
                # Record the process execution for the Gantt chart
                self.execution_log.append({
                    "pid": shortest_process.pid,
                    "start": shortest_process.start_time,
                    "duration": shortest_process.burst_time,
                    "color": shortest_process.color,
                    "response_time": shortest_process.response_time, 
                    "queue_length": len(available_processes) 
                })

                remaining_processes.remove(shortest_process)
            else:
                current_time += 1  # Increment time if no processes are available yet

    def sjf_preemptive(self):
        """Shortest Job First (Preemptive) Scheduling"""
        print("Running SJF (Preemptive) Scheduling...")
        current_time = 0
        remaining_processes = sorted(self.processes, key=lambda p: p.arrival_time)
        ready_queue = []
        last_process = None  # Track the last executed process

        while remaining_processes or ready_queue:
            # Move processes from remaining_processes to ready_queue as time passes
            while remaining_processes and remaining_processes[0].arrival_time <= current_time:
                ready_queue.append(remaining_processes.pop(0))

            # Record the queue length
            self.queue_lengths.append(len(ready_queue))

            if ready_queue:
                # Sort ready_queue by remaining burst time
                ready_queue.sort(key=lambda p: p.remaining_time)
                # Pick the process with the shortest remaining burst time
                shortest_process = ready_queue[0]

                if shortest_process.start_time == -1:  # This means the process hasn't started yet
                    shortest_process.start_time = current_time
                    shortest_process.response_time = shortest_process.start_time - shortest_process.arrival_time  # Calculate response time
                    self.response_times.append(shortest_process.response_time)  # Add to response_times
                    if last_process != shortest_process:  # If it's a different process, increment context switch
                        self.context_switches += 1
                    # print(f"Process {shortest_process.pid} started at {shortest_process.start_time}")

                # Execute process for 1 time unit
                start_time = current_time
                shortest_process.remaining_time -= 1
                current_time += 1

                # Record the process execution for the Gantt chart
                self.execution_log.append({
                    "pid": shortest_process.pid,
                    "start": start_time,
                    "duration": 1,  # 1 time unit per step in preemptive SJF
                    "color": shortest_process.color,
                    "response_time": shortest_process.response_time, 
                    "queue_length": len(ready_queue)  
                })

                if shortest_process.remaining_time == 0:
                    shortest_process.completion_time = current_time
                    shortest_process.turnaround_time = shortest_process.completion_time - shortest_process.arrival_time
                    shortest_process.waiting_time = shortest_process.turnaround_time - shortest_process.burst_time
                    ready_queue.remove(shortest_process)  # Process is completed and removed from queue

                # Update the last executed process
                last_process = shortest_process
            else:
                current_time += 1  # Increment time if no processes are ready

    def priority_scheduling(self):
        """Priority Scheduling (Non-preemptive)"""
        print("Priority Scheduling (Non-preemptive)...")
        current_time = 0
        remaining_processes = sorted(self.processes, key=lambda p: (p.arrival_time, p.priority))

        while remaining_processes:
            # Find processes that have arrived and sort by priority
            available_processes = [p for p in remaining_processes if p.arrival_time <= current_time]

            # Record the queue length
            self.queue_lengths.append(len(available_processes))

            if available_processes:
                # Choose the process with the highest priority (lowest priority number)
                highest_priority_process = min(available_processes, key=lambda p: p.priority)
                if current_time < highest_priority_process.arrival_time:
                    current_time = highest_priority_process.arrival_time

                # Set start time if not already set
                if highest_priority_process.start_time == -1:
                    highest_priority_process.start_time = current_time
                    highest_priority_process.response_time = highest_priority_process.start_time - highest_priority_process.arrival_time
                    self.response_times.append(highest_priority_process.response_time)

                # Update waiting time
                highest_priority_process.waiting_time = current_time - highest_priority_process.arrival_time

                # Execute the process
                current_time += highest_priority_process.burst_time
                highest_priority_process.completion_time = current_time
                highest_priority_process.turnaround_time = highest_priority_process.completion_time - highest_priority_process.arrival_time

                # Record the process execution for the Gantt chart
                self.execution_log.append({
                    "pid": highest_priority_process.pid,
                    "start": highest_priority_process.start_time,
                    "duration": highest_priority_process.burst_time,
                    "color": highest_priority_process.color,
                    "response_time": highest_priority_process.response_time, 
                    "queue_length": len(available_processes)  
                })

                remaining_processes.remove(highest_priority_process)
            else:
                # Increment time if no processes are available yet
                self.execution_log.append({
                    "pid": "I",  # Idle
                    "start": current_time,
                    "duration": 1,
                    "color": "#D3D3D3",  # Idle color
                    "response_time": None,  # Idle has no response time
                    "queue_length": len(remaining_processes)  # Remaining processes count
                })
                current_time += 1


    def round_robin(self, quantum):
            """Round Robin Scheduling with time slicing"""
            print("Round Robin Scheduling...")

            # Initialize the log to record the execution of each time slice
            self.execution_log = []

            # Sort the processes by arrival time
            queue = sorted(self.processes, key=lambda p: p.arrival_time)
            current_time = 0

            while queue:
                has_executed = False  # Flag to indicate whether any process has executed at the current time
                for process in list(queue):
                    if process.arrival_time <= current_time:
                        # Process can be executed

                        # If the process's start_time has not been set, set it to the current time
                        if process.start_time == -1:
                            process.start_time = current_time
                            process.response_time = process.start_time - process.arrival_time  # Calculate response time
                            self.response_times.append(process.response_time)  # Add to response_times

                        # Record the start time and time slice
                        start_time = current_time
                        time_slice = min(process.remaining_time, quantum)
                        process.remaining_time -= time_slice
                        current_time += time_slice
                        has_executed = True

                        # Log the execution details
                        self.execution_log.append({
                            "pid": process.pid,
                            "start": start_time,
                            "duration": time_slice,
                            "color": process.color
                        })

                        # If the process is not finished, move it back to the queue
                        if process.remaining_time > 0:
                            queue.append(queue.pop(0))  # Move this process to the end of the queue
                            self.context_switches += 1  # Count the context switch
                            # print(f"Context switch at time {current_time}")
                        else:
                            # Process has completed
                            process.completion_time = current_time
                            process.turnaround_time = process.completion_time - process.arrival_time
                            process.waiting_time = process.turnaround_time - process.burst_time
                            queue.remove(process)

                    else:
                        continue

                if not has_executed:
                    # If no processes can be executed, add an idle time slice
                    self.execution_log.append({
                        "pid": "I",
                        "start": current_time,
                        "duration": 1,
                        "color": "#D3D3D3",  # Idle color
                        "response_time": process.response_time,  # Add response time
                        "queue_length": len(queue)  # Add the length of the queue

                    })
                    current_time += 1


    def get_context_switches(self):
        return self.context_switches
