import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 定义任务数据 (任务ID, 开始时间, 结束时间)
tasks = [
    {"id": 1, "start": 5, "end": 13},
    {"id": 2, "start": 13, "end": 17},
    {"id": 3, "start": 0, "end": 5},
    {"id": 4, "start": 17, "end": 20},
    {"id": 5, "start": 20, "end": 26},
]

# 提取时间轴和设置绘图
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 30)  # 时间范围
ax.set_ylim(0, len(tasks) + 1)  # 任务数量
ax.set_yticks(range(1, len(tasks) + 1))  # y轴显示任务编号
ax.set_yticklabels([f"任务 {task['id']}" for task in tasks])  # 任务标签
ax.set_xlabel("时间")
ax.set_title("任务调度动画")

bars = []

# 初始化任务条（每个任务的进度条）
for i, task in enumerate(tasks):
    bar = ax.barh(i + 1, 0, height=0.5, color="green", align="center")  # 初始宽度为0
    bars.append(bar)

# 动画更新函数
def update(frame):
    for i, task in enumerate(tasks):
        if task["start"] <= frame <= task["end"]:  # 当前时间处于任务执行阶段
            bars[i].patches[0].set_width(frame - task["start"])
        elif frame > task["end"]:  # 当前时间超过任务结束时间
            bars[i].patches[0].set_width(task["end"] - task["start"])

# 创建动画
ani = FuncAnimation(fig, update, frames=range(30), interval=200, repeat=False)

# 保存动画为GIF文件
ani.save("任务调度动画.gif", writer="pillow")
plt.show()