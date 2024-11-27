import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def show_gantt(tasks):
    """显示动态甘特图弹窗"""
    # 创建弹窗
    popup = tk.Toplevel()
    popup.title("Dynamic Gantt Chart")
    popup.geometry("800x400")

    # 初始化Matplotlib绘图
    fig, ax = plt.subplots(figsize=(8, 4))
    canvas = FigureCanvasTkAgg(fig, master=popup)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # 动态绘图参数
    current_time = 0
    max_time = max(task["start"] + task["duration"] for task in tasks)
    interval = 100  # 每帧更新间隔（毫秒） -> 增大以减慢速度
    time_step = 0.2  # 每帧推进时间 -> 减小以减慢速度

    def update(frame):
        nonlocal current_time
        current_time += time_step

        ax.clear()
        ax.set_title("Dynamic Gantt Chart")
        ax.set_xlabel("Time")
        ax.set_ylabel("Tasks")
        ax.set_xlim(0, max_time)
        ax.set_ylim(0, len(tasks) + 1)

        # 绘制任务进度条
        for i, task in enumerate(tasks):
            task_end = min(current_time, task["start"] + task["duration"])
            if current_time >= task["start"]:  # 当前时间已到任务开始时间
                progress = task_end - task["start"]
                ax.barh(i + 1, progress, left=task["start"], color="blue")
                ax.text(task["start"] + progress / 2, i + 1, task["name"], va="center", ha="center", color="white")

        canvas.draw()
        if current_time >= max_time:
            ani.event_source.stop()

    # 启动动画
    ani = FuncAnimation(fig, update, frames=range(0, int(max_time / time_step)), interval=interval, repeat=False)

# 主窗口（用于触发弹窗）
root = tk.Tk()
root.title("Main Window")

# 测试任务数据
tasks = [
    {"name": "Task 1", "start": 0, "duration": 5},
    {"name": "Task 2", "start": 5, "duration": 3},
    {"name": "Task 3", "start": 8, "duration": 7},
]

# 显示弹窗并运行动画
root.after(1000, lambda: show_gantt(tasks))  # 1秒后弹窗
root.mainloop()
