# src/gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from scheduler import Scheduler
from process import Process
from matplotlib.animation import FuncAnimation
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1400x800")
        self.processes = []
        self.previous_processes = []  
        self.scheduler = Scheduler(self.processes)
        self.input_entries = []
        self.figure = None 
        self.canvas = None 
        self.ani = None  
        self.configure_root()
        self.create_widgets()

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

        self.output_text = tk.Text(output_frame, height=10, wrap="word", font=("Helvetica", 14))
        self.output_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.config(yscrollcommand=scrollbar.set)

    def create_metrics_frame(self):
        """Create the performance metrics display frame"""
        self.metrics_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.metrics_frame.grid(row=6, column=3, columnspan=1, sticky="nsew", padx=10, pady=10)

        # Add title label
        self.metrics_title = tk.Label(self.metrics_frame, text="Performance Metrics", font=("Helvetica", 16, "bold"), bg="#f4f4f4")
        self.metrics_title.grid(row=0, column=0, columnspan=2, pady=10)

        # Add labels for displaying performance metrics
        self.avg_waiting_time_label = tk.Label(self.metrics_frame, text="Average Waiting Time:", font=("Helvetica", 14), bg="#f4f4f4")
        self.avg_waiting_time_label.grid(row=1, column=0, sticky="w", pady=5)

        self.avg_turnaround_time_label = tk.Label(self.metrics_frame, text="Average Turnaround Time:", font=("Helvetica", 14), bg="#f4f4f4")
        self.avg_turnaround_time_label.grid(row=2, column=0, sticky="w", pady=5)

        self.context_switches_label = tk.Label(self.metrics_frame, text="Context Switches:", font=("Helvetica", 14), bg="#f4f4f4")
        self.context_switches_label.grid(row=3, column=0, sticky="w", pady=5)

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
        for i, task in enumerate(tasks):
            task_start = task["start"]
            task_end = task["start"] + task["duration"]

            # Draw bars only if the current time is greater than the task start time
            if current_time >= task_start:
                progress = min(current_time - task_start, task["duration"])  # Dynamic bar length
                self.ax.barh(i + 1, progress, left=task_start, color=task["color"], edgecolor="black")
                
                # Display task name inside the bar
                self.ax.text(
                    task_start + progress / 2, i + 1, task["name"],
                    va="center", ha="center", color="black", fontweight="bold"
                )
                
                # Add start time label
                self.ax.text(
                    task_start, i + 1.2, f"Start: {task_start}",
                    va="center", ha="center", fontsize=10, color="black"
                )

                # Add end time label (only when the task is completed)
                if current_time >= task_end:
                    self.ax.text(
                        task_end, i + 1.2, f"End: {task_end}",
                        va="center", ha="center", fontsize=10, color="black"
                    )

        # Set time range and task range
        max_time = max(task["start"] + task["duration"] for task in tasks)
        self.ax.set_xlim(0, max_time + 1)  # Time axis range
        self.ax.set_ylim(0, len(tasks) + 1)  # Task range
        self.canvas.draw()  # Update the figure

    def show_gantt_chart(self, tasks):
        """Display the Gantt chart animation"""
        max_time = max(task["start"] + task["duration"] for task in tasks)
        time_step = 0.2  # Time step per frame
        interval = 100   # Frame update interval (milliseconds)

        # Stop any existing animation
        if self.ani is not None:
            if self.ani.event_source is not None:  # Ensure event_source exists
                self.ani.event_source.stop()  # Stop the previous animation
            self.ani = None  # Clear the animation object

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

        # Make sure the time slice is a valid number (applicable only to Round Robin)
        if algorithm == "Round Robin" and (not time_quantum.isdigit() or int(time_quantum) <= 0):
            messagebox.showerror("Error", "Please enter a valid positive integer for the time quantum.")
            return

        # Initialize the scheduler and process
        scheduler = Scheduler(self.processes)
        quantum = int(time_quantum) if time_quantum.isdigit() else None

        # Call the corresponding scheduling algorithm
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

        # Save the current process list to previous_processes
        self.previous_processes = [Process(p.pid, p.arrival_time, p.burst_time, p.priority) for p in self.processes]
        # Collecting performance metrics
        avg_waiting_time = sum(p.waiting_time for p in self.processes) / len(self.processes)
        avg_turnaround_time = sum(p.turnaround_time for p in self.processes) / len(self.processes)
        context_switches = scheduler.get_context_switches()

        # Update performance indicator display
        self.avg_waiting_time_label.config(text=f"Average Waiting Time: {avg_waiting_time:.2f}")
        self.avg_turnaround_time_label.config(text=f"Average Turnaround Time: {avg_turnaround_time:.2f}")
        self.context_switches_label.config(text=f"Context Switches: {context_switches}")

        # Update Output Area
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Scheduling Algorithm: {algorithm}\n\n")
        for process in self.processes:
            self.output_text.insert(
                tk.END,
                f"Process {process.pid} -> Arrival: {process.arrival_time}, "
                f"Burst: {process.burst_time}, Start: {process.start_time}, "
                f"Completion: {process.completion_time}, Waiting: {process.waiting_time}, "
                f"Turnaround: {process.turnaround_time}\n"
            )
                
        # Update Gantt chart
        tasks = [
            {
                "name": process.pid,
                "start": process.start_time,
                "duration": process.burst_time,
                "color": process.color,
            }
            for process in self.processes
        ]
        self.show_gantt_chart(tasks)
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