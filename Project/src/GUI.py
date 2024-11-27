# src/gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from scheduler import Scheduler
from process import Process
from matplotlib.animation import FuncAnimation

class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1400x800")
        self.processes = []
        self.scheduler = Scheduler(self.processes)
        self.input_entries = []

        self.configure_root()
        self.create_widgets()

        #self.canvas = tk.Canvas(self.root, width=1000, height=400)
        #self.canvas.grid(row=6, column=0, columnspan=2, pady=15, sticky="nsew")

    def configure_root(self):
        """配置主窗口的背景颜色和网格布局"""
        self.root.configure(bg="#f4f4f4")
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(5, weight=1)  # 输出区域
        self.root.grid_rowconfigure(6, weight=1)  # 甘特图区域

    def create_widgets(self):
        self.create_title()
        self.create_input_section()
        self.create_buttons()
        self.create_algorithm_selection()
        self.create_output_area()
        self.create_metrics_frame()
        # 创建 Canvas 用于绘制甘特图
        self.canvas = tk.Canvas(self.root,bg="white")
        self.canvas.grid(row=6, column=0, columnspan=3, pady=15, sticky="nsew")

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

        self.output_text = tk.Text(output_frame, height=10, wrap="word", font=("Helvetica", 14))
        self.output_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.config(yscrollcommand=scrollbar.set)

    def create_metrics_frame(self):
        """创建性能指标显示框"""
        self.metrics_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.metrics_frame.grid(row=6, column=3, columnspan=1, sticky="nsew", padx=10, pady=10)

        # 添加标题标签
        self.metrics_title = tk.Label(self.metrics_frame, text="Performance Metrics", font=("Helvetica", 16, "bold"), bg="#f4f4f4")
        self.metrics_title.grid(row=0, column=0, columnspan=2, pady=10)

        # 预留标签用于展示性能指标
        self.avg_waiting_time_label = tk.Label(self.metrics_frame, text="Average Waiting Time:", font=("Helvetica", 14), bg="#f4f4f4")
        self.avg_waiting_time_label.grid(row=1, column=0, sticky="w", pady=5)

        self.avg_turnaround_time_label = tk.Label(self.metrics_frame, text="Average Turnaround Time:", font=("Helvetica", 14), bg="#f4f4f4")
        self.avg_turnaround_time_label.grid(row=2, column=0, sticky="w", pady=5)

        self.context_switches_label = tk.Label(self.metrics_frame, text="Context Switches:", font=("Helvetica", 14), bg="#f4f4f4")
        self.context_switches_label.grid(row=3, column=0, sticky="w", pady=5)

    def animate_gantt_chart(self, step=0, max_finish_time=0):
        """更新甘特图"""
        self.canvas.delete("all")  # 每次重绘之前清除画布
        #self.canvas.create_text(1100, 20, text="Performance Metrics", font=("Arial", 14, "bold"))

        # 绘制性能指标
        self.display_metrics_on_canvas()

        # 绘制甘特图的横坐标时间线
        self.canvas.create_line(100, 100, max_finish_time * 40 + 100, 100, width=2)

        # 绘制每个进程的执行条
        for i, process in enumerate(self.processes):
            if process.completion_time > step:
                start_x = process.start_time * 40 + 100  # 每个时间单位宽度为40
                end_x = process.completion_time * 40 + 100
                self.canvas.create_rectangle(start_x, 100 + i * 30, end_x, 130 + i * 30, fill="blue")
                self.canvas.create_text(start_x + (end_x - start_x) / 2, 115 + i * 30, text=f"P{process.pid}")

        # 每50ms更新一次甘特图（通过after）
        if step < max_finish_time:
            self.root.after(500, self.animate_gantt_chart, step + 1, max_finish_time)

    def display_metrics_on_canvas(self):
        """显示性能指标"""
        metrics = {
            "Average Waiting Time": sum(p.waiting_time for p in self.processes) / len(self.processes),
            "Average Turnaround Time": sum(p.turnaround_time for p in self.processes) / len(self.processes),
            "Context Switches": self.scheduler.get_context_switches(),
        }
        y_position = 40  # 设置文本起始位置
        for metric, value in metrics.items():
            self.canvas.create_text(1100, y_position, text=f"{metric}: {value:.2f}", anchor="w", font=("Arial", 12))
            y_position += 20

    def add_process(self):
        try:
            # 获取输入的值
            pid = self.process_id.get()
            arrival = int(self.arrival_time.get())
            burst = int(self.burst_time.get())
            priority = int(self.priority.get())

            # 检查 process_id 是否重复
            if any(process.pid == pid for process in self.processes):
                messagebox.showerror("Duplicate Process ID", f"Process ID '{pid}' already exists. Please use a unique ID.")
                return  # 如果重复，退出方法

            # 创建新的进程并添加到列表
            process = Process(pid, arrival, burst, priority)
            self.processes.append(process)

            # 显示成功添加的信息
            self.output_text.insert(tk.END, f"Added Process: {pid}, Arrival: {arrival}, Burst: {burst}, Priority: {priority}\n")
            
            # 清空输入框
            self.process_id.delete(0, tk.END)
            self.arrival_time.delete(0, tk.END)
            self.burst_time.delete(0, tk.END)
            self.priority.delete(0, tk.END)
        except ValueError:
            # 显示输入错误提示
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
        avg_waiting_time = sum(p.waiting_time for p in self.processes) / len(self.processes)
        avg_turnaround_time = sum(p.turnaround_time for p in self.processes) / len(self.processes)
        context_switches = scheduler.get_context_switches()

        # 更新性能指标显示
        self.avg_waiting_time_label.config(text=f"Average Waiting Time: {avg_waiting_time:.2f}")
        self.avg_turnaround_time_label.config(text=f"Average Turnaround Time: {avg_turnaround_time:.2f}")
        self.context_switches_label.config(text=f"Context Switches: {context_switches}")

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

        # 启动动画
        max_finish_time = max(p.completion_time for p in self.processes) + 1
        self.animate_gantt_chart(0, max_finish_time)

    def display_metrics(self, metrics):
        """显示性能指标"""
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()  # 清除旧的指标

        tk.Label(self.metrics_frame, text="Performance Metrics", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2)

        row = 1
        for metric, value in metrics.items():
            tk.Label(self.metrics_frame, text=f"{metric}:", font=("Helvetica", 16)).grid(row=row, column=0, padx=10, sticky="W")
            tk.Label(self.metrics_frame, text=f"{value:.2f}", font=("Helvetica", 16)).grid(row=row, column=1, padx=10, sticky="E")
            row += 1
    
    def create_entry(self, row, column):
        """创建输入框并绑定箭头键事件"""
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
    def increase_output_font(self):
        """Increase the font size of the output area"""
        current_font = self.output_text.cget("font")
        family, size, *rest = current_font.split()
        new_size = int(size) + 2  # 增加字体大小
        self.output_text.configure(font=(family, new_size))
    def decrease_output_font(self):
        """Reducing the font size of the output area"""
        current_font = self.output_text.cget("font")
        family, size, *rest = current_font.split()
        new_size = max(10, int(size) - 2)  # Make sure the font size is not less than 10
        self.output_text.configure(font=(family, new_size))

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()
