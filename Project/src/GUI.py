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
        self.root.geometry("1000x700")  # 设置默认窗口大小

        # 配置列的权重
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(5, weight=1)  # 输出区域占据更多空间

        self.processes = []

        # 设置字体和背景颜色
        self.root.configure(bg="#f4f4f4")  # 背景浅灰色
        default_font = ("Helvetica", 12)

        # 标题
        title = tk.Label(root, text="CPU Scheduling Simulator", font=("Helvetica", 18, "bold"), bg="#f4f4f4")
        title.grid(row=0, column=0, columnspan=4, pady=20)

        # 输入区域
        tk.Label(root, text="Process ID", font=default_font, bg="#f4f4f4").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(root, text="Arrival Time", font=default_font, bg="#f4f4f4").grid(row=1, column=1, padx=10, pady=5)
        tk.Label(root, text="Burst Time", font=default_font, bg="#f4f4f4").grid(row=1, column=2, padx=10, pady=5)
        tk.Label(root, text="Priority", font=default_font, bg="#f4f4f4").grid(row=1, column=3, padx=10, pady=5)

        self.process_id = tk.Entry(root, font=default_font)
        self.arrival_time = tk.Entry(root, font=default_font)
        self.burst_time = tk.Entry(root, font=default_font)
        self.priority = tk.Entry(root, font=default_font)

        self.process_id.grid(row=2, column=0, padx=10, pady=5)
        self.arrival_time.grid(row=2, column=1, padx=10, pady=5)
        self.burst_time.grid(row=2, column=2, padx=10, pady=5)
        self.priority.grid(row=2, column=3, padx=10, pady=5)

        # 按钮区域
        add_process_btn = tk.Button(root, text="Add Process", font=default_font, bg="#d9ead3", command=self.add_process)
        add_process_btn.grid(row=3, column=0, pady=15)

        run_simulation_btn = tk.Button(root, text="Run Simulation", font=default_font, bg="#c9daf8", command=self.run_simulation)
        run_simulation_btn.grid(row=3, column=3, pady=15)

        # 算法选择区域
        tk.Label(root, text="Choose Algorithm", font=default_font, bg="#f4f4f4").grid(row=4, column=0, pady=10)
        self.algorithm_var = tk.StringVar()
        algorithms = ["FCFS", "SJF-Non", "SJF-Preemptive", "Priority Scheduling", "Round Robin"]
        self.algorithm_menu = ttk.Combobox(root, textvariable=self.algorithm_var, values=algorithms, font=default_font)
        self.algorithm_menu.grid(row=4, column=1, padx=10, pady=5)

        # 时间片输入
        tk.Label(root, text="Time Quantum (for RR)", font=default_font, bg="#f4f4f4").grid(row=4, column=2, padx=10)
        self.time_quantum = tk.Entry(root, font=default_font)
        self.time_quantum.grid(row=4, column=3, padx=10)

        # 输出区域
        output_frame = tk.Frame(root)
        output_frame.grid(row=5, column=0, columnspan=4, pady=15, sticky="nsew")
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        self.output_text = tk.Text(output_frame, height=20, wrap="word", font=("Helvetica", 10))
        self.output_text.grid(row=0, column=0, sticky="nsew")

        # 滚动条
        scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.config(yscrollcommand=scrollbar.set)

    def add_process(self):
        try:
            pid = self.process_id.get()
            arrival = int(self.arrival_time.get())
            burst = int(self.burst_time.get())
            priority = int(self.priority.get())

            process = Process(pid, arrival, burst, priority)
            self.processes.append(process)

            self.output_text.insert(tk.END, f"Added Process: {pid}, Arrival: {arrival}, Burst: {burst}, Priority: {priority}\n")
            self.process_id.delete(0, tk.END)
            self.arrival_time.delete(0, tk.END)
            self.burst_time.delete(0, tk.END)
            self.priority.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values for Arrival, Burst, and Priority times.")

    def run_simulation(self):
        algorithm = self.algorithm_var.get()
        if not algorithm:
            messagebox.showerror("Algorithm Error", "Please select a scheduling algorithm.")
            return

        scheduler = Scheduler(self.processes)

        try:
            if algorithm == "FCFS":
                scheduler.fcfs()
            elif algorithm == "SJF-Non":
                scheduler.sjf_non_preemptive()
            elif algorithm == "SJF-Preemptive":
                scheduler.sjf_preemptive()
            elif algorithm == "Priority Scheduling":
                scheduler.priority_scheduling()
            elif algorithm == "Round Robin":
                quantum = int(self.time_quantum.get())
                scheduler.round_robin(quantum)
            else:
                raise ValueError("Unsupported algorithm")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        context_switches = scheduler.get_context_switches()
        metrics = calculate_metrics(self.processes, context_switches)

        self.output_text.insert(tk.END, "\n--- Simulation Results ---\n")
        for process in self.processes:
            self.output_text.insert(tk.END, f"Process {process.pid}: Start Time: {process.start_time}, Waiting Time: {process.waiting_time}, Turnaround Time: {process.turnaround_time}\n")

        self.output_text.insert(tk.END, "\n--- Performance Metrics ---\n")
        for metric, value in metrics.items():
            self.output_text.insert(tk.END, f"{metric}: {value}\n")

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




