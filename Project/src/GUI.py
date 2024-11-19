# src/gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from scheduler import Scheduler
from process import Process
import matplotlib.pyplot as plt
from metrics import calculate_metrics, plot_gantt_chart, plot_histograms
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.processes = []

        # Increase window size for a larger interface
        self.root.geometry("900x700")

        # Title Label
        title = tk.Label(root, text="CPU Scheduling Simulator", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, pady=20)

        # Process input fields
        tk.Label(root, text="Process ID").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(root, text="Arrival Time").grid(row=1, column=1, padx=10, pady=10)
        tk.Label(root, text="Burst Time").grid(row=1, column=2, padx=10, pady=10)
        tk.Label(root, text="Priority").grid(row=1, column=3, padx=10, pady=10)

        self.process_id = tk.Entry(root)
        self.arrival_time = tk.Entry(root)
        self.burst_time = tk.Entry(root)
        self.priority = tk.Entry(root)

        self.process_id.grid(row=2, column=0, padx=10)
        self.arrival_time.grid(row=2, column=1, padx=10)
        self.burst_time.grid(row=2, column=2, padx=10)
        self.priority.grid(row=2, column=3, padx=10)

        # Buttons for adding processes and running simulation
        add_process_btn = tk.Button(root, text="Add Process", command=self.add_process)
        add_process_btn.grid(row=3, column=0, pady=15)

        run_simulation_btn = tk.Button(root, text="Run Simulation", command=self.run_simulation)
        run_simulation_btn.grid(row=3, column=3, pady=15)

        # Algorithm Selection
        tk.Label(root, text="Choose Algorithm").grid(row=4, column=0, pady=10)
        self.algorithm_var = tk.StringVar()
        algorithms = ["FCFS", "SJF-Non", "SJF-Preemptive", "Priority Scheduling", "Round Robin"]
        self.algorithm_menu = ttk.Combobox(root, textvariable=self.algorithm_var, values=algorithms)
        self.algorithm_menu.grid(row=4, column=1, padx=10)

        # Quantum input for Round Robin
        tk.Label(root, text="Time Quantum (for RR)").grid(row=4, column=2, padx=10)
        self.time_quantum = tk.Entry(root)
        self.time_quantum.grid(row=4, column=3, padx=10)

        # Output display for results
        self.output_text = tk.Text(root, height=20, width=80)  # Increased size
        self.output_text.grid(row=5, column=0, columnspan=4, pady=15)

    def add_process(self):
        try:
            # Extract and validate process inputs
            pid = self.process_id.get()
            arrival = int(self.arrival_time.get())
            burst = int(self.burst_time.get())
            priority = int(self.priority.get())

            # Create and add process to list
            process = Process(pid, arrival, burst, priority)
            self.processes.append(process)

            # Display added process
            self.output_text.insert(tk.END,
                                    f"Added Process: {pid}, Arrival: {arrival}, Burst: {burst}, Priority: {priority}\n")

            # Clear inputs
            self.process_id.delete(0, tk.END)
            self.arrival_time.delete(0, tk.END)
            self.burst_time.delete(0, tk.END)
            self.priority.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Input Error",
                                 "Please enter valid integer values for Arrival, Burst, and Priority times.")

    def run_simulation(self):
        # Select algorithm
        algorithm = self.algorithm_var.get()
        if not algorithm:
            messagebox.showerror("Algorithm Error", "Please select a scheduling algorithm.")
            return

        # Create a Scheduler instance with current processes
        scheduler = Scheduler(self.processes)

        # Execute selected algorithm
        if algorithm == "FCFS":
            scheduler.fcfs()
        elif algorithm == "SJF-Non":
            scheduler.sjf_non_preemptive()
        elif algorithm == "SJF-Preemptive":
            scheduler.sjf_preemptive()
        elif algorithm == "Priority Scheduling":
            scheduler.priority_scheduling()
        elif algorithm == "Round Robin":
            try:
                quantum = int(self.time_quantum.get())
                scheduler.round_robin(quantum)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid integer for Time Quantum.")
                return

        # Get context switches from the scheduler
        context_switches = scheduler.get_context_switches()

        # Calculate metrics after scheduling
        metrics = calculate_metrics(self.processes, context_switches)

        # Display the results
        self.output_text.insert(tk.END, "\n--- Simulation Results ---\n")
        for process in self.processes:
            self.output_text.insert(tk.END, f"Process {process.pid}: Start Time: {process.start_time}, "
                                            f"Waiting Time: {process.waiting_time}, "
                                            f"Turnaround Time: {process.turnaround_time}\n")

        # Display performance metrics
        self.output_text.insert(tk.END, "\n--- Performance Metrics ---\n")
        for metric, value in metrics.items():
            self.output_text.insert(tk.END, f"{metric}: {value}\n")

        # Reset processes for next run
        self.processes.clear()

    def display_metrics(self, metrics):
        # Display each metric in a more compact way
        pass

    def display_gantt_chart(self):
        # Generate Gantt chart figure
        fig, ax = plt.subplots()
        plot_gantt_chart(self.processes)

        # Embed chart in GUI
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, column=0, columnspan=4)

    def display_histograms(self):
        # Generate histogram figure
        fig, ax = plt.subplots()
        plot_histograms(self.processes)

        # Embed histogram in GUI
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=6, column=0, columnspan=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()
