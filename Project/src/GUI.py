# Updated GUI.py with dynamic animation

import tkinter as tk
from tkinter import ttk, messagebox
from scheduler import Scheduler
from process import Process


class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1400x800")
        self.processes = []
        self.scheduler = Scheduler(self.processes)
        self.input_entries = []
        self.animation_running = False  # 用于控制动画状态

        self.configure_root()
        self.create_widgets()

    def configure_root(self):
        """配置主窗口的背景颜色和网格布局"""
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
        self.canvas = tk.Canvas(self.root, width=1200, height=400, bg="white")
        self.canvas.grid(row=6, column=0, columnspan=4, pady=15, sticky="nsew")

    def create_title(self):
        """创建标题标签"""
        title = tk.Label(
            self.root,
            text="CPU Scheduling Simulator",
            font=("Helvetica", 20, "bold"),
            bg="#f4f4f4"
        )
        title.grid(row=0, column=0, columnspan=4, pady=20)

    def create_input_section(self):
        """创建输入区域，包括标签和输入框"""
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
        """创建按钮区域"""
        tk.Button(
            self.root, text="Add Process", font=("Helvetica", 18),
            bg="#d9ead3", command=self.add_process
        ).grid(row=3, column=0, pady=15)

        tk.Button(
            self.root, text="Run Simulation", font=("Helvetica", 18),
            bg="#c9daf8", command=self.run_simulation
        ).grid(row=3, column=3, pady=15)

    def create_algorithm_selection(self):
        """创建算法选择和时间片输入区域"""
        tk.Label(
            self.root, text="Choose Algorithm", font=("Helvetica", 18), bg="#f4f4f4"
        ).grid(row=4, column=0, pady=10)

        self.algorithm_var = tk.StringVar()
        algorithms = ["FCFS", "SJF-Non", "SJF-Preemptive", "Priority Scheduling", "Round Robin"]
        self.algorithm_menu = ttk.Combobox(
            self.root, textvariable=self.algorithm_var, values=algorithms, font=("Helvetica", 18)
        )
        self.algorithm_menu.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(
            self.root, text="Time Quantum (for RR)", font=("Helvetica", 18), bg="#f4f4f4"
        ).grid(row=4, column=2, padx=10)

        self.time_quantum = tk.Entry(self.root, font=("Helvetica", 18))
        self.time_quantum.grid(row=4, column=3, padx=10)

    def create_output_area(self):
        """创建输出区域，包括滚动条"""
        output_frame = tk.Frame(self.root)
        output_frame.grid(row=5, column=0, columnspan=4, pady=15, sticky="nsew")
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        self.output_text = tk.Text(output_frame, height=20, wrap="word", font=("Helvetica", 14))
        self.output_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.config(yscrollcommand=scrollbar.set)

    def create_metrics_frame(self):
        """创建性能指标显示框"""
        self.metrics_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.metrics_frame.grid(row=6, column=2, columnspan=2, sticky="nsew", padx=10, pady=10)

    def draw_gantt_chart(self, step):
        """动态绘制甘特图"""
        self.canvas.delete("all")
        time_scale = 40  # 每单位时间40像素
        bar_height = 40  # 每个任务的条形高度

        for i, process in enumerate(self.processes):
            start_x = process.start_time * time_scale
            y_top = i * bar_height + 20
            y_bottom = y_top + bar_height

            if step < process.start_time:  # 当前时间还未到任务开始时间
                continue

            # 动态显示任务条形宽度，直到任务结束时间
            end_x = min(step, process.completion_time) * time_scale

            # 绘制任务条形
            self.canvas.create_rectangle(start_x, y_top, end_x, y_bottom, fill=process.color, outline="black")

            # 在条形中间显示进程ID
            self.canvas.create_text(
                (start_x + end_x) / 2, y_top + bar_height / 2,
                text=f"P{process.pid}", fill="white", font=("Helvetica", 14)
            )

            # 显示开始时间和结束时间标签
            self.canvas.create_text(
                start_x, y_bottom + 10, text=f"Start: {process.start_time}", anchor="w", font=("Helvetica", 10)
            )
            if step >= process.completion_time:  # 仅在任务结束后显示结束时间
                self.canvas.create_text(
                    process.completion_time * time_scale, y_bottom + 10,
                    text=f"End: {process.completion_time}", anchor="e", font=("Helvetica", 10)
                )

    def animate_gantt_chart(self, current_time=0):
        """更新甘特图的动画逻辑"""
        max_time = max(p.completion_time for p in self.processes)
        self.draw_gantt_chart(current_time)  # 绘制当前时间的甘特图
        if current_time < max_time:  # 如果当前时间小于最大完成时间
            self.root.after(500, self.animate_gantt_chart, current_time + 1)  # 延迟调用下一帧
            
    def add_process(self):
        """添加进程"""
        try:
            pid = self.process_id.get()
            arrival = int(self.arrival_time.get())
            burst = int(self.burst_time.get())
            priority = int(self.priority.get())
            if any(process.pid == pid for process in self.processes):
                messagebox.showerror("Error", "Duplicate Process ID")
                return
            process = Process(pid, arrival, burst, priority)
            self.processes.append(process)
            self.output_text.insert(tk.END, f"Added Process: {pid}, Arrival: {arrival}, Burst: {burst}, Priority: {priority}\n")
            for entry in self.input_entries:
                entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
    def create_entry(self, row, column):
        """创建输入框并绑定箭头键事件"""
        entry = tk.Entry(self.root, font=("Helvetica", 14))
        entry.grid(row=row, column=column, padx=10, pady=5)
        return entry

    def run_simulation(self):
        """运行选定的调度算法"""
        algorithm = self.algorithm_var.get()
        time_quantum = self.time_quantum.get()

        if not algorithm:
            messagebox.showerror("Error", "Select an algorithm")
            return

        scheduler = Scheduler(self.processes)
        if algorithm == "FCFS":
            scheduler.fcfs()
        elif algorithm == "SJF-Non":
            scheduler.sjf_non_preemptive()
        elif algorithm == "SJF-Preemptive":
            scheduler.sjf_preemptive()
        elif algorithm == "Priority Scheduling":
            scheduler.priority_scheduling()
        elif algorithm == "Round Robin":
            if not time_quantum.isdigit():
                messagebox.showerror("Error", "Invalid Time Quantum")
                return
            scheduler.round_robin(int(time_quantum))

        # 显示结果
        self.output_text.delete("1.0", tk.END)
        for process in self.processes:
            self.output_text.insert(
                tk.END,
                f"P{process.pid}: Arrival={process.arrival_time}, Start={process.start_time}, "
                f"Completion={process.completion_time}, Waiting={process.waiting_time}, "
                f"Turnaround={process.turnaround_time}\n"
            )
        self.animate_gantt_chart(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()