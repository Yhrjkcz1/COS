
class Scheduler:
    def __init__(self, processes):
        self.processes = processes
        self.context_switches = 0  # Initialize context_switches as an instance variable
        self.execution_log = []  # To store the logs for Gantt chart

    def fcfs(self):
        """First-Come-First-Serve (FCFS) Scheduling"""
        print("First-Come-First-Serve (FCFS) Scheduling...")
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

            # Record the process execution for the Gantt chart
            self.execution_log.append({
                "pid": process.pid,
                "start": process.start_time,
                "duration": process.burst_time,
                "color": process.color
            })

    def sjf_non_preemptive(self):
        """Shortest Job First (Non-preemptive) Scheduling"""
        print("Running SJF (Non-preemptive) Scheduling...")
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

                # Record the process execution for the Gantt chart
                self.execution_log.append({
                    "pid": shortest_process.pid,
                    "start": shortest_process.start_time,
                    "duration": shortest_process.burst_time,
                    "color": shortest_process.color
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

        while remaining_processes or ready_queue:
            # Move processes from remaining_processes to ready_queue as time passes
            while remaining_processes and remaining_processes[0].arrival_time <= current_time:
                ready_queue.append(remaining_processes.pop(0))

            if ready_queue:
                # Sort ready_queue by remaining burst time
                ready_queue.sort(key=lambda p: p.remaining_time)
                # Pick the process with the shortest remaining burst time
                shortest_process = ready_queue[0]

                if shortest_process.start_time == -1:  # This means the process hasn't started yet
                    shortest_process.start_time = current_time
                    self.context_switches += 1  # Increment context switch
                    print(f"Process {shortest_process.pid} started at {shortest_process.start_time}")

                # Execute process for 1 time unit
                start_time = current_time
                shortest_process.remaining_time -= 1
                current_time += 1

                # Record the process execution for the Gantt chart
                self.execution_log.append({
                    "pid": shortest_process.pid,
                    "start": start_time,
                    "duration": 1,  # 1 time unit per step in preemptive SJF
                    "color": shortest_process.color
                })

                if shortest_process.remaining_time == 0:
                    shortest_process.completion_time = current_time
                    shortest_process.turnaround_time = shortest_process.completion_time - shortest_process.arrival_time
                    shortest_process.waiting_time = shortest_process.turnaround_time - shortest_process.burst_time
                    ready_queue.remove(shortest_process)  # Process is completed and removed from queue
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

                # Record the process execution for the Gantt chart
                self.execution_log.append({
                    "pid": highest_priority_process.pid,
                    "start": highest_priority_process.start_time,
                    "duration": highest_priority_process.burst_time,
                    "color": highest_priority_process.color
                })

                remaining_processes.remove(highest_priority_process)
            else:
                current_time += 1  # Increment time if no processes are available yet

    def round_robin(self, quantum):
        """Round Robin Scheduling with time slicing"""
        print("Round Robin Scheduling...")

        # 初始化日志以记录每个时间片的执行
        self.execution_log = []

        # 按到达时间排序进程
        queue = sorted(self.processes, key=lambda p: p.arrival_time)
        current_time = 0

        while queue:
            has_executed = False  # 标记当前时间是否有进程被执行
            for process in list(queue):
                if process.arrival_time <= current_time:
                    # 进程可以执行

                    # 如果进程的start_time还未被设置，则设置为当前时间
                    if process.start_time == -1:
                        process.start_time = current_time

                    # 记录开始时间和时间片
                    start_time = current_time
                    time_slice = min(process.remaining_time, quantum)
                    process.remaining_time -= time_slice
                    current_time += time_slice
                    has_executed = True

                    # 记录日志
                    self.execution_log.append({
                        "pid": process.pid,
                        "start": start_time,
                        "duration": time_slice,
                        "color": process.color
                    })

                    if process.remaining_time == 0:
                        # 进程完成
                        process.completion_time = current_time
                        process.turnaround_time = process.completion_time - process.arrival_time
                        process.waiting_time = process.turnaround_time - process.burst_time
                        queue.remove(process)
                else:
                    continue

            if not has_executed:
                # 如果当前没有进程可以运行，增加空闲时间片
                self.execution_log.append({
                    "pid": "Idle",
                    "start": current_time,
                    "duration": 1,
                    "color": "#D3D3D3"  # Idle color
                })
                current_time += 1


    def get_context_switches(self):
        # Ensure context_switches is properly returned
        return self.context_switches
