# src/metrics.py

import matplotlib.pyplot as plt

def calculate_metrics(processes, context_switches):
    total_waiting_time = sum(p.waiting_time for p in processes)
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    n = len(processes)

    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n
    cpu_utilization = (sum(p.burst_time for p in processes) / max(p.completion_time for p in processes)) * 100
    throughput = n / max(p.completion_time for p in processes)

    return {
        "Average Waiting Time": avg_waiting_time,
        "Average Turnaround Time": avg_turnaround_time,
        "CPU Utilization (%)": cpu_utilization,
        "Throughput": throughput,
        "Context Switches": context_switches
    }

def plot_gantt_chart(processes):
    plt.figure(figsize=(10, 6))
    plt.barh([p.pid for p in processes], [p.burst_time for p in processes],
             left=[p.start_time for p in processes], color="skyblue", edgecolor="black")
    plt.xlabel("Time")
    plt.ylabel("Process ID")
    plt.title("Process Execution Timeline (Gantt Chart)")
    plt.show()

def plot_histograms(processes):
    waiting_times = [p.waiting_time for p in processes]
    turnaround_times = [p.turnaround_time for p in processes]

    plt.figure(figsize=(12, 5))

    # Histogram of Waiting Times
    plt.subplot(1, 2, 1)
    plt.hist(waiting_times, bins=10, color="lightcoral", edgecolor="black")
    plt.xlabel("Waiting Time")
    plt.ylabel("Frequency")
    plt.title("Histogram of Waiting Times")

    # Histogram of Turnaround Times
    plt.subplot(1, 2, 2)
    plt.hist(turnaround_times, bins=10, color="lightgreen", edgecolor="black")
    plt.xlabel("Turnaround Time")
    plt.ylabel("Frequency")
    plt.title("Histogram of Turnaround Times")

    plt.tight_layout()
    plt.show()

#