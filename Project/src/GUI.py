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
        self.input_entries = []  # 用于存储输入框的引用

        # 设置字体和背景颜色
        self.root.configure(bg="#f4f4f4")  # 背景浅灰色
        default_font = ("Helvetica", 16)

        # 标题
        title = tk.Label(root, text="CPU Scheduling Simulator", font=("Helvetica", 20, "bold"), bg="#f4f4f4")
        title.grid(row=0, column=0, columnspan=4, pady=20)

        # 输入区域
        tk.Label(root, text="Process ID", font=default_font, bg="#f4f4f4").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(root, text="Arrival Time", font=default_font, bg="#f4f4f4").grid(row=1, column=1, padx=10, pady=5)
        tk.Label(root, text="Burst Time", font=default_font, bg="#f4f4f4").grid(row=1, column=2, padx=10, pady=5)
        tk.Label(root, text="Priority", font=default_font, bg="#f4f4f4").grid(row=1, column=3, padx=10, pady=5)
        # 输入框
        self.process_id = self.create_entry(root, row=2, column=0)
        self.arrival_time = self.create_entry(root, row=2, column=1)
        self.burst_time = self.create_entry(root, row=2, column=2)
        self.priority = self.create_entry(root, row=2, column=3)
        # 添加到输入框列表
        self.input_entries = [
            self.process_id,
            self.arrival_time,
            self.burst_time,
            self.priority
        ]

        self.process_id.grid(row=2, column=0, padx=10, pady=5)
        self.arrival_time.grid(row=2, column=1, padx=10, pady=5)
        self.burst_time.grid(row=2, column=2, padx=10, pady=5)
        self.priority.grid(row=2, column=3, padx=10, pady=5)

        # 按钮区域
        add_process_btn = tk.Button(root, text="Add Process", font=default_font, bg="#d9ead3", command=self.add_process)
        add_process_btn.grid(row=3, column=0, pady=15)

        run_simulation_btn = tk.Button(root, text="Run Simulation", font=default_font, bg="#c9daf8", command=self.run_simulation)
        run_simulation_btn.grid(row=3, column=3, pady=15)
        # 字体放大按钮
        increase_font_btn = tk.Button(root, text="Increase Font Size", font=default_font, command=self.increase_output_font)
        increase_font_btn.grid(row=7, column=0, pady=10)
        # 字体缩小按钮
        decrease_font_btn = tk.Button(root, text="Decrease Font Size", font=default_font, command=self.decrease_output_font)
        decrease_font_btn.grid(row=7, column=1, pady=10)

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

        self.output_text = tk.Text(output_frame, height=20, wrap="word", font=("Helvetica", 14))
        self.output_text.grid(row=0, column=0, sticky="nsew")
        # 输出区域
        self.metrics_frame = tk.Frame(root, bg="#f4f4f4")
        self.metrics_frame.grid(row=6, column=0, columnspan=2, sticky="nsew")

        self.figure_frame = tk.Frame(root, bg="#f4f4f4")
        self.figure_frame.grid(row=6, column=2, columnspan=2, sticky="nsew")

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
        """运行选定的调度算法并更新 GUI"""
        algorithm = self.algorithm_var.get()
        time_quantum = self.time_quantum.get()

        if not algorithm:
            messagebox.showerror("Error", "Please select a scheduling algorithm.")
            return

        # 确保时间片是有效数字（仅适用于 Round Robin）
        if algorithm == "Round Robin" and (not time_quantum.isdigit() or int(time_quantum) <= 0):
            messagebox.showerror("Error", "Please enter a valid positive integer for the time quantum.")
            return

        # 初始化调度器和进程
        scheduler = Scheduler(self.processes)
        quantum = int(time_quantum) if time_quantum.isdigit() else None

        # 调用相应的调度算法
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

        # 收集性能指标
        metrics = {
            "Average Waiting Time": sum(p.waiting_time for p in self.processes) / len(self.processes),
            "Average Turnaround Time": sum(p.turnaround_time for p in self.processes) / len(self.processes),
            "Context Switches": scheduler.get_context_switches(),
        }

        # 更新输出区域
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

        # 调用图形更新
        self.display_metrics(metrics)           # 显示性能指标
        self.display_gantt_chart(self.processes)  # 显示甘特图
        self.display_histograms(self.processes)  # 显示直方图

    def display_metrics(self, metrics):
        """显示性能指标"""
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()  # 清除旧的指标

        tk.Label(self.metrics_frame, text="Performance Metrics", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2)

        row = 1
        for metric, value in metrics.items():
            tk.Label(self.metrics_frame, text=f"{metric}:").grid(row=row, column=0, padx=10, sticky="W")
            tk.Label(self.metrics_frame, text=f"{value:.2f}").grid(row=row, column=1, padx=10, sticky="E")
            row += 1

    def display_gantt_chart(self, processes):
        """显示甘特图"""
        for widget in self.figure_frame.winfo_children():
            widget.destroy()  # 清除旧图表

        fig, ax = plt.subplots(figsize=(8, 4))
        # 假设 plot_gantt_chart 是一个生成甘特图的函数
        plot_gantt_chart(processes, ax)

        canvas = FigureCanvasTkAgg(fig, master=self.figure_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def display_histograms(self, processes):
        """显示直方图"""
        for widget in self.figure_frame.winfo_children():
            widget.destroy()  # 清除旧图表

        fig, ax = plt.subplots(figsize=(8, 4))
        # 假设 plot_histograms 是一个生成直方图的函数
        plot_histograms(processes, ax)

        canvas = FigureCanvasTkAgg(fig, master=self.figure_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        # 添加 Entry 并绑定方向键事件
    def create_entry(self, root, row, column):
        entry = tk.Entry(root)
        entry.grid(row=row, column=column, padx=10, pady=5)

        # 绑定箭头键事件
        entry.bind("<Up>", self.focus_up)
        entry.bind("<Down>", self.focus_down)
        entry.bind("<Left>", self.focus_left)
        entry.bind("<Right>", self.focus_right)
        return entry

    def focus_up(self, event):
        index = self.input_entries.index(event.widget)
        if index >= 4:  # 确保至少有一行在上方
            self.input_entries[index - 4].focus_set()

    def focus_down(self, event):
        index = self.input_entries.index(event.widget)
        if index + 4 < len(self.input_entries):  # 确保有一行在下方
            self.input_entries[index + 4].focus_set()

    def focus_left(self, event):
        index = self.input_entries.index(event.widget)
        if index % 4 != 0:  # 确保不是最左列
            self.input_entries[index - 1].focus_set()

    def focus_right(self, event):
        index = self.input_entries.index(event.widget)
        if index % 4 != 3 and index + 1 < len(self.input_entries):  # 确保不是最右列
            self.input_entries[index + 1].focus_set()
    def increase_output_font(self):
        """增加输出区域的字体大小"""
        current_font = self.output_text.cget("font")
        family, size, *rest = current_font.split()
        new_size = int(size) + 2  # 增加字体大小
        self.output_text.configure(font=(family, new_size))
    def decrease_output_font(self):
        """缩小输出区域的字体大小"""
        current_font = self.output_text.cget("font")
        family, size, *rest = current_font.split()
        new_size = max(10, int(size) - 2)  # 保证字体大小不小于 10
        self.output_text.configure(font=(family, new_size))

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()