# src/gui.py
import copy
import tkinter as tk
from tkinter import ttk, messagebox
from scheduler import Scheduler
from process import Process
from visual import Visualizer
from matplotlib.animation import FuncAnimation
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1400x1200")
        self.processes = []
        self.previous_processes = []  
        self.scheduler = Scheduler(self.processes)
        self.input_entries = []
        self.figure = None 
        self.canvas = None 
        self.ani = None  
        self.initial_processes = None
        self.y_positions = {} 
        self.configure_root()
        self.create_widgets()
        self.visualizer = Visualizer()
         
    def configure_root(self):
        """Configure the background color and grid layout of the main window"""
        self.root.configure(bg="#f4f4f4")
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(5, weight=1)  
        self.root.grid_rowconfigure(6, weight=1)  

    def create_widgets(self):
        self.create_title()
        self.create_input_section()
        self.create_buttons()
        self.create_algorithm_selection()
        self.create_output_area()
        self.create_metrics_frame()
        self.create_gantt_chart_area() 
        self.current_gantt_window = None
 
    def create_title(self):
        """Create a title tag"""
        title = tk.Label(
            self.root,
            text="CPU Scheduling Simulator",
            font=("Helvetica", 20, "bold"),
            bg="#f4f4f4"
        )
        title.grid(row=0, column=0, columnspan=4, pady=20)

    def create_input_section(self):
        """Create an input area, including a label and an input box"""
        labels = ["Process ID", "Arrival Time", "Burst Time", "Priority"]
        for i, text in enumerate(labels):
            tk.Label(
                self.root, text=text, font=("Helvetica", 18), bg="#f4f4f4"
            ).grid(row=1, column=i, padx=10, pady=5)

        self.process_id = self.create_entry(2, 0)
        self.arrival_time = self.create_entry(2, 1)
        self.burst_time = self.create_entry(2, 2)
        self.priority = self.create_entry(2, 3)
        self.input_entries = [self.process_id, self.arrival_time, self.burst_time, self.priority]

    def create_buttons(self):
        """Create the buttons area"""
        add_process_btn = tk.Button(
            self.root, text="Add Process", font=("Helvetica", 18),
            bg="#d9ead3", command=self.add_process
        )
        add_process_btn.grid(row=3, column=0, pady=15)

        run_simulation_btn = tk.Button(
            self.root, text="Run Simulation", font=("Helvetica", 18),
            bg="#c9daf8", command=self.run_simulation
        )
        run_simulation_btn.grid(row=3, column=3, pady=15)

        # Add random generate and reset buttons
        random_btn = tk.Button(
            self.root, text="Random Generate", font=("Helvetica", 18),
            bg="#fce5cd", command=self.generate_random_processes
        )
        random_btn.grid(row=3, column=1, pady=10, padx=5)

        # Create a frame for Reset and Reload buttons
        control_frame = tk.Frame(self.root, bg="#f4f4f4")
        control_frame.grid(row=3, column=2, pady=10, padx=5)

        # Reset button
        reset_btn = tk.Button(
            control_frame, text="Reset", font=("Helvetica", 18),
            bg="#f4cccc", command=self.reset_simulation
        )
        reset_btn.pack(side="left", padx=5)

        # Reload button
        reload_btn = tk.Button(
            control_frame, text="Reload", font=("Helvetica", 18),
            bg="#d9d9f3", command=self.reload_last_simulation
        )
        reload_btn.pack(side="left", padx=5)

    def create_algorithm_selection(self):
        """Create algorithm selection and time quantum input area"""
        tk.Label(
            self.root, text="Choose Algorithm", font=("Helvetica", 18), bg="#f4f4f4"
        ).grid(row=4, column=0, pady=10)

        self.algorithm_var = tk.StringVar()
        algorithms = ["FCFS", "SJF-Non", "SJF-Preemptive", "Priority Scheduling", "Round Robin"]
        self.algorithm_menu = ttk.Combobox(
            self.root, textvariable=self.algorithm_var, values=algorithms, font=("Helvetica", 18)
        )
        self.algorithm_menu.grid(row=4, column=1, padx=10, pady=5)

        # Bind the algorithm selection change event
        self.algorithm_menu.bind("<<ComboboxSelected>>", self.validate_time_quantum)

        tk.Label(
            self.root, text="Time Quantum (for RR)", font=("Helvetica", 18), bg="#f4f4f4"
        ).grid(row=4, column=2, padx=10)

        self.time_quantum = tk.Entry(self.root, font=("Helvetica", 18))
        self.time_quantum.grid(row=4, column=3, padx=10)

        # Initial validation on load (set based on default algorithm)
        self.validate_time_quantum()

    def generate_random_processes(self):
        """Randomly generate 5 example processes and update the interface"""
        self.processes.clear()  # Clear the current process list
        for i in range(5):
            pid = f"P{i + 1}"
            arrival_time = random.randint(0, 10)
            burst_time = random.randint(1, 10)
            priority = random.randint(1, 5)
            process = Process(pid, arrival_time, burst_time, priority)
            self.processes.append(process)

        # Update the output area
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "Randomly Generated Processes:\n")
        for process in self.processes:
            self.output_text.insert(
                tk.END, f"Process {process.pid}: Arrival={process.arrival_time}, "
                        f"Burst={process.burst_time}, Priority={process.priority}\n"
            )

    def reset_simulation(self):
        """Clear all data and reset the interface"""
        self.processes.clear()  # Clear the process list

        # Clear input fields and output area
        for entry in self.input_entries:
            entry.delete(0, tk.END)
        self.output_text.delete("1.0", tk.END)

        # Destroy the Gantt chart (if it exists)
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        # Recreate the Gantt chart area
        self.create_gantt_chart_area()

        # Reset performance metrics
        self.avg_waiting_time_label.config(text="Average Waiting Time:")
        self.avg_turnaround_time_label.config(text="Average Turnaround Time:")
        self.context_switches_label.config(text="Context Switches:")

        # Clear algorithm selection and time quantum
        self.algorithm_var.set("")
        self.time_quantum.delete(0, tk.END)
        
    def restart_simulation(self):
        """Reset simulation state but retain user input processes"""
        # Clear previous performance metrics
        self.processes = copy.deepcopy(self.initial_processes)
        self.visualizer.performance_metrics=[]
        self.scheduler.execution_log = [] 
        self.context_switches = 0
        self.output_text.delete("1.0", tk.END)
        self.current_gantt_window = None
        # Destroy the Gantt chart (if it exists)
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        # for process in self.processes:
        #     process.start_time = None
        #     process.completion_time = None
        #     process.waiting_time = None
        #     process.turnaround_time = None
        #     process.response_time = None
        # Recreate the Gantt chart area
        self.create_gantt_chart_area()

        # Reset performance metrics display
        self.avg_waiting_time_label.config(text="Average Waiting Time:")
        self.avg_turnaround_time_label.config(text="Average Turnaround Time:")
        self.context_switches_label.config(text="Context Switches:")

        # Retain process input data (no need to clear the `self.processes` list)
        self.output_text.insert(tk.END, "Simulation state cleared. Ready to run again with existing processes.\n")

    def reload_last_simulation(self):
        """Reload the process data from the last run"""
        if not self.previous_processes:
            messagebox.showinfo("Reload Error", "No previous processes to reload.")
            return

        self.processes = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in self.previous_processes]

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "Reloaded Previous Processes:\n")
        for process in self.processes:
            self.output_text.insert(
                tk.END, f"Process {process.pid}: Arrival={process.arrival_time}, "
                        f"Burst={process.burst_time}, Priority={process.priority}\n"
            )

    def create_output_area(self):
        """Creates the output area, including scroll bars"""
        output_frame = tk.Frame(self.root)
        output_frame.grid(row=5, column=0, columnspan=4, pady=15, sticky="nsew")
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        self.output_text = tk.Text(output_frame, height=10, wrap="word", font=("Consolas", 15))
        self.output_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.config(yscrollcommand=scrollbar.set)

    def create_metrics_frame(self):  
        """Create the performance metrics display frame"""
        self.metrics_frame = tk.Frame(self.root, bg="#f4f4f4", width=50, height=50)  # Fixed size
        self.metrics_frame.grid(row=6, column=3, columnspan=1, sticky="nsew", padx=10, pady=10)

        # Add title label
        self.metrics_title = tk.Label(self.metrics_frame, text="Performance Metrics", font=("Helvetica", 16, "bold"), bg="#f4f4f4")
        self.metrics_title.grid(row=0, column=0, columnspan=2, pady=10)

        # Add labels for displaying performance metrics
        self.avg_waiting_time_label = tk.Label(self.metrics_frame, text="Average Waiting Time:", font=("Helvetica", 14), bg="#f4f4f4")
        self.avg_waiting_time_label.grid(row=1, column=0, sticky="w", pady=5)

        self.avg_turnaround_time_label = tk.Label(self.metrics_frame, text="Average Turnaround Time:", font=("Helvetica", 14), bg="#f4f4f4")
        self.avg_turnaround_time_label.grid(row=2, column=0, sticky="w", pady=5)

        self.avg_response_time_label = tk.Label(self.metrics_frame, text="Average Response Time:", font=("Helvetica", 14), bg="#f4f4f4")
        self.avg_response_time_label.grid(row=3, column=0, sticky="w", pady=5)

        self.context_switches_label = tk.Label(self.metrics_frame, text="Context Switches:", font=("Helvetica", 14), bg="#f4f4f4")
        self.context_switches_label.grid(row=4, column=0, sticky="w", pady=5)

        # Add comparison title label (placed below the Performance Metrics section)
        self.comparison_title = tk.Label(self.metrics_frame, text="Algorithm Comparison", font=("Helvetica", 16, "bold"), bg="#f4f4f4")
        self.comparison_title.grid(row=5, column=0, columnspan=2, pady=10)

        # Create buttons for metrics comparison (placed in rows below "Algorithm Comparison")
        button1 = tk.Button(
            self.metrics_frame, text="Waiting Time", font=("Helvetica", 14),
            bg="#d9ead3", command=self.plot_avg_waiting_time
        )
        button1.grid(row=6, column=0, pady=8, padx=2)

        button2 = tk.Button(
            self.metrics_frame, text="Turnaround Time", font=("Helvetica", 14),
            bg="#c9daf8", command=self.plot_avg_turnaround_time
        )
        button2.grid(row=6, column=1, pady=8, padx=2, sticky="ew")

        button3 = tk.Button(
            self.metrics_frame, text="Response Time", font=("Helvetica", 14),
            bg="#fce5cd", command=self.plot_avg_response_time
        )
        button3.grid(row=7, column=0, pady=8, padx=2)

        button4 = tk.Button(
            self.metrics_frame, text="Radar Compare", font=("Helvetica", 14),
            bg="#f4cccc", command=self.plot_radar_chart
        )
        button4.grid(row=7, column=1, pady=8, padx=2, sticky="ew")

        # Set equal column width by configuring grid columns (keep columns fixed)
        self.metrics_frame.grid_columnconfigure(0, weight=0, minsize=25)  # Don't let the column expand
        self.metrics_frame.grid_columnconfigure(1, weight=0, minsize=25)  # Same for the second column
        self.metrics_frame.grid_rowconfigure(0, weight=0)  # Don't let the row expand either
        self.metrics_frame.grid_rowconfigure(1, weight=0)
        self.metrics_frame.grid_rowconfigure(2, weight=0)
        self.metrics_frame.grid_rowconfigure(3, weight=0)
        self.metrics_frame.grid_rowconfigure(4, weight=0)
        self.metrics_frame.grid_rowconfigure(5, weight=0)
        self.metrics_frame.grid_rowconfigure(6, weight=0)
        self.metrics_frame.grid_rowconfigure(7, weight=0)

    def create_gantt_chart_area(self):
        """Create the Gantt chart area in the GUI"""
        # Initialize the Matplotlib figure
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.set_title("Dynamic Gantt Chart")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Processes")

        # Embed the chart into Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=3, pady=15, sticky="nsew")

    def update_gantt_chart(self, frame, tasks, time_step):
        """Update the Gantt chart dynamically"""
        current_time = frame * time_step  # Current time
        self.ax.clear()  # Clear previous content
        self.ax.set_title("Dynamic Gantt Chart")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Processes")

        # Draw task progress bars
        for task in tasks:
            task_start = task["start"]
            task_end = task["start"] + task["duration"]

            # Ensure color is valid
            color = task["color"]

            # Get the y position for the current task's pid (sorted by unique pid)
            y_pos = self.y_positions.get(task["pid"], None)

            # If pid has not been assigned a y_pos, assign one
            if y_pos is None:
                y_pos = len(self.y_positions) + 1
                self.y_positions[task["pid"]] = y_pos

            # Draw bars only if the current time is greater than the task start time
            if current_time >= task_start:
                progress = min(current_time - task_start, task["duration"])  # Dynamic bar length
                self.ax.barh(y_pos, progress, left=task_start, color=color, edgecolor="black")

                # Display task name inside the bar
                self.ax.text(
                    task_start + progress / 2, y_pos, task["pid"],
                    va="center", ha="center", color="black", fontweight="bold"
                )

                # Add start time label
                self.ax.text(
                    task_start, y_pos + 0.7, f"S: {task_start}",
                    va="top", ha="center", fontsize=10, color="black"
                )

                # Add end time label when the task is completed or on the last frame
                if current_time >= task_end or frame == int((max(t["start"] + t["duration"] for t in tasks)) / time_step) - 1:
                    self.ax.text(
                        task_end, y_pos - 0.7, f"E: {task_end}",
                        va="bottom", ha="center", fontsize=10, color="black"
                    )

        # Set time range and task range
        max_time = max(task["start"] + task["duration"] for task in tasks)
        self.ax.set_xlim(0, max_time + 1)  # Time axis range
        self.ax.set_ylim(0, len(self.y_positions) + 1)  # Task range based on unique y positions
        self.canvas.draw()  # Update the figure

    def show_gantt_chart(self, tasks):
        """Display the Gantt chart animation"""
        
        if hasattr(self, "current_gantt_window") and self.current_gantt_window is not None:
            plt.close(self.current_gantt_window)
            self.current_gantt_window = None
        # Initialize y_positions as an empty dictionary to keep track of y-axis positions for unique pids
        self.y_positions = {}
        tasks.sort(key=lambda x: x["pid"])
        # Check if 'Idle' exists in the tasks
        has_idle = any(task["pid"] == "I" for task in tasks)
        
        # Assign y position starting from 1 for processes, and 0 for Idle if it exists
        next_y_pos = 1  # Start assigning y positions from 1
        
        for task in tasks:

            # Ensure that each task has 'pid' key
            if "pid" not in task:
                print(f"Warning: Task {task} does not have 'pid' key")
                continue
            
            pid = task["pid"]
            
            if pid == "I" and "I" not in self.y_positions:
                # If Idle exists, assign it y=0
                self.y_positions[pid] = 0
            elif pid not in self.y_positions:
                # If it's not Idle, assign the next available y position starting from 1
                self.y_positions[pid] = next_y_pos
                next_y_pos += 1  # Increment for the next process

        max_time = max(task["start"] + task["duration"] for task in tasks)
        time_step = 0.4  # Time step per frame
        interval = 100   # Frame update interval (milliseconds)

        # Stop any existing animation
        if self.ani is not None:
            if self.ani.event_source is not None:
                self.ani.event_source.stop()
            self.ani = None
        self.current_gantt_window = self.figure
        # Start a new animation
        frames = int(max_time / time_step)

        self.ani = FuncAnimation(
            self.figure, self.update_gantt_chart,
            frames=frames, interval=interval, repeat=False,
            fargs=(tasks, time_step)
        )

    def add_process(self):
        try:
            # Get the value of the input
            pid = self.process_id.get()
            arrival = int(self.arrival_time.get())
            burst = int(self.burst_time.get())
            priority = int(self.priority.get())

            # check if is process_id duplicate
            if any(process.pid == pid for process in self.processes):
                messagebox.showerror("Duplicate Process ID", f"Process ID '{pid}' already exists. Please use a unique ID.")
                return  

            # Create a new process and add it to the list
            process = Process(pid, arrival, burst, priority)
            self.processes.append(process)

            # Displays information about successful addition
            self.output_text.insert(tk.END, f"Added Process: {pid}, Arrival: {arrival}, Burst: {burst}, Priority: {priority}\n")
            
            # Clear the input box
            self.process_id.delete(0, tk.END)
            self.arrival_time.delete(0, tk.END)
            self.burst_time.delete(0, tk.END)
            self.priority.delete(0, tk.END)
        except ValueError:
            # Display input error message
            messagebox.showerror("Input Error", "Please enter valid integer values for Arrival, Burst, and Priority times.")

    def run_simulation(self):
        """Runs the selected scheduling algorithm and updates the GUI"""
        algorithm = self.algorithm_var.get()
        time_quantum = self.time_quantum.get()
        if not algorithm:
            messagebox.showerror("Error", "Please select a scheduling algorithm.")
            return
        if not self.processes:
            messagebox.showerror("Error", "No tasks to process. Please check your input.")
            return
        # print("Initial state of self.processes:")
        # if not self.processes or len(self.processes) == 0:
        #     print("self.processes is empty.")
        # else:
        #     for process in self.processes:
        #         print(f"PID: {process.pid}, Arrival: {process.arrival_time}, Burst: {process.burst_time}, Priority: {process.priority}")
        plt.close(self.current_gantt_window)
        if not hasattr(self, 'initial_processes') or self.initial_processes is None or self.input_has_changed():
            if self.current_gantt_window:
                plt.close(self.current_gantt_window)
                print("Closing current gantt window.")
                self.current_gantt_window = None 
            self.initial_processes = copy.deepcopy(self.processes)
            print("Initial processes saved:")
            for process in self.initial_processes:
                print(f"PID: {process.pid}, Arrival: {process.arrival_time}, Burst: {process.burst_time}, Priority: {process.priority}")
        else:
            print("Initial processes already exist.")

        self.restart_simulation()
        if not self.processes:
            print("Error: No processes to calculate performance metrics2.")
            return

         # Remaining scheduling logic...
        # print("Processes before running algorithm:")
        # for process in self.processes:
        #     print(f"PID: {process.pid}, Arrival: {process.arrival_time}, Burst: {process.burst_time}, Priority: {process.priority}")

        # Validate the time slice for Round Robin
        if algorithm == "Round Robin" and (not time_quantum.isdigit() or int(time_quantum) <= 0):
            messagebox.showerror("Error", "Please enter a valid positive integer for the time quantum.")
            return
        # Initialize the scheduler and processes
        scheduler = Scheduler(self.processes)
        quantum = int(time_quantum) if time_quantum.isdigit() else None

        # Run the selected scheduling algorithm
        if algorithm == "FCFS":
            scheduler.fcfs()
        elif algorithm == "SJF-Non":
            scheduler.sjf_non_preemptive()
        elif algorithm == "SJF-Preemptive":
            scheduler.sjf_preemptive()
        elif algorithm == "Priority Scheduling":
            scheduler.priority_scheduling()
        elif algorithm == "Round Robin":
            scheduler.round_robin(quantum)

        # Save the current processes state
        self.previous_processes = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in self.processes]

        # Calculate performance metrics
        avg_waiting_time = sum(p.waiting_time for p in self.processes) / len(self.processes)
        avg_turnaround_time = sum(p.turnaround_time for p in self.processes) / len(self.processes)
        context_switches = scheduler.get_context_switches()
        # Calculate average response time
        avg_response_time = sum(p.response_time for p in self.processes if p.response_time is not None) / len(self.processes)

        # Update GUI with performance metrics
        self.avg_waiting_time_label.config(text=f"Average Waiting Time: {avg_waiting_time:.2f}")
        self.avg_turnaround_time_label.config(text=f"Average Turnaround Time: {avg_turnaround_time:.2f}")
        self.avg_response_time_label.config(text=f"Average Response Time: {avg_response_time:.2f}")  # Add this line
        self.context_switches_label.config(text=f"Context Switches: {context_switches}")

        # Update output area
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Scheduling Algorithm: {algorithm}\n\n")
        for process in self.processes:
            self.output_text.insert(
                tk.END,
                f"Process {process.pid:>2} -> "
                f"Arrival: {process.arrival_time:>2}, "
                f"Burst: {process.burst_time:>2}, "
                f"Priority: {process.priority:>2}, "
                f"Start: {process.start_time:>2}, "
                f"Completion: {process.completion_time:>2}, "
                f"Waiting: {process.waiting_time:>2}, "
                f"Turnaround: {process.turnaround_time:>2}, "
                f"Response: {process.response_time:>2}\n"
            )

        # Update Gantt chart with time-sliced tasks
        tasks = [
            {
                "pid": log["pid"] if log["pid"] != "I" else "I",
                "start": log["start"],
                "duration": log["duration"],
                "color": log["color"] if log["pid"] != "I" else "grey",
                "response_time": log.get("response_time", None),  # Add response_time
                "queue_length": log.get("queue_length", None)  # Add queue_length
            }
            for log in scheduler.execution_log  # Assuming round_robin populates execution_log
        ]
        if hasattr(self, "current_gantt_window") and self.current_gantt_window is not None:
            plt.close(self.current_gantt_window)
            self.current_gantt_window = None
        self.show_gantt_chart(tasks)
        # print("Processes before running visual:")
        # for process in self.processes:
        #     print(f"Process {process.pid} attributes:")
        #     for attr, value in vars(process).items():
        #         print(f"  {attr}: {value}")
        #     print("-" * 40)  # Separator for better readability

        #     # Pass a deep copy of processes to run_all_algorithms
        processes_copy = copy.deepcopy(self.processes)
        scheduler_copy = copy.deepcopy(self.scheduler)
        self.visualizer.run_all_algorithms(scheduler_copy.processes, scheduler_copy)
        # print("Processes after running visual:")
        # for process in self.processes:
        #     print(f"Process {process.pid} attributes:")
        #     for attr, value in vars(process).items():
        #         print(f"  {attr}: {value}")
        #     print("-" * 40)  # Separator for better readability

    def input_has_changed(self):
        """Check if the user has provided new task input."""
        if not hasattr(self, 'initial_processes') or not self.initial_processes:
            return True  # No initial processes saved yet
        
        # Compare current processes with initial processes
        if len(self.processes) != len(self.initial_processes):
            return True

        for p1, p2 in zip(self.processes, self.initial_processes):
            if (p1.pid != p2.pid or
                p1.arrival_time != p2.arrival_time or
                p1.burst_time != p2.burst_time or
                p1.priority != p2.priority):
                return True

        return False

    def validate_time_quantum(self, event=None):
        """Validate the Time Quantum field based on selected algorithm"""
        selected_algorithm = self.algorithm_var.get()

        if selected_algorithm == "Round Robin":
            # Enable the time quantum entry field if "Round Robin" is selected
            self.time_quantum.config(state="normal")
        else:
            # Disable the time quantum entry field and clear it if another algorithm is selected
            self.time_quantum.config(state="disabled")
            self.time_quantum.delete(0, tk.END)

    def display_metrics(self, metrics):
        """Display performance indicators"""
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()  # Clear old metrics

        tk.Label(self.metrics_frame, text="Performance Metrics", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2)

        row = 1
        for metric, value in metrics.items():
            tk.Label(self.metrics_frame, text=f"{metric}:", font=("Helvetica", 16)).grid(row=row, column=0, padx=10, sticky="W")
            tk.Label(self.metrics_frame, text=f"{value:.2f}", font=("Helvetica", 16)).grid(row=row, column=1, padx=10, sticky="E")
            row += 1

    def plot_avg_waiting_time(self):
        if self.current_gantt_window:
            plt.close(self.current_gantt_window)
            self.current_gantt_window = None  
        self.visualizer.plot_avg_waiting_time() 

    def plot_avg_turnaround_time(self):
        if self.current_gantt_window:
            plt.close(self.current_gantt_window)
            self.current_gantt_window = None  
        self.visualizer.plot_avg_turnaround_time() 

    def plot_avg_response_time(self):
        if self.current_gantt_window:
            plt.close(self.current_gantt_window)
            self.current_gantt_window = None  
        self.visualizer.plot_avg_response_time()  

    def plot_radar_chart(self):
        if self.current_gantt_window:
            plt.close(self.current_gantt_window)
            self.current_gantt_window = None  
        self.visualizer.plot_radar_chart()

    def plot_overall_comparison(self):
        self.visualizer.plot_overall_comparison()  
    def create_entry(self, row, column):
        """Create an input box and bind arrow key events"""
        entry = tk.Entry(self.root, font=("Helvetica", 14))
        entry.grid(row=row, column=column, padx=10, pady=5)
        entry.bind("<Up>", self.focus_up)
        entry.bind("<Down>", self.focus_down)
        entry.bind("<Left>", self.focus_left)
        entry.bind("<Right>", self.focus_right)
        return entry
    def focus_up(self, event):
        index = self.input_entries.index(event.widget)
        if index >= 4:  # Make sure there is at least one line on top
            self.input_entries[index - 4].focus_set()
    def focus_down(self, event):
        index = self.input_entries.index(event.widget)
        if index + 4 < len(self.input_entries):  
            self.input_entries[index + 4].focus_set()
    def focus_left(self, event):
        index = self.input_entries.index(event.widget)
        if index % 4 != 0:  
            self.input_entries[index - 1].focus_set()
    def focus_right(self, event):
        index = self.input_entries.index(event.widget)
        if index % 4 != 3 and index + 1 < len(self.input_entries): 
            self.input_entries[index + 1].focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()