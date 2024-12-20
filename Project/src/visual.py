import matplotlib.pyplot as plt
from scheduler import Scheduler
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
class Visualizer:
    def __init__(self):
        self.performance_metrics = []
        self.current_figure = None
        self.current_gantt_window = None
        self.ani = None 
        self.figure = None 
        self.canvas = None

    def run_all_algorithms(self, task_set, scheduler):
        """Run all algorithms on the same task set and collect performance data"""
        
        # List of algorithms with an indication of whether they are Round Robin
        algorithms = [
            ("FCFS", scheduler.fcfs, None),  # No quantum for non-Round Robin
            ("SJF-Non", scheduler.sjf_non_preemptive, None),
            ("SJF-Pree", scheduler.sjf_preemptive, None),
            ("Priority Scheduling", scheduler.priority_scheduling, None),
            ("RR", scheduler.round_robin, [1, 2, 3]),  # Round Robin with quantum values
        ]
        
        self.performance_metrics = []  # To store performance data for each algorithm

        # Run each algorithm and collect performance metrics
        for algo_name, algo_func, quantum_values in algorithms:
            # Reset the state of each task before running a new algorithm
            if quantum_values:  # If the algorithm is Round Robin (has quantum values)
                for quantum in quantum_values:
                    for task in task_set:
                         task.reset_state()
                    algo_func(quantum)  # Run Round Robin with the current quantum value
                    avg_waiting_time = sum(task.waiting_time for task in task_set) / len(task_set)
                    avg_turnaround_time = sum(task.turnaround_time for task in task_set) / len(task_set)
                    avg_response_time = sum(task.response_time for task in task_set) / len(task_set)

                    self.performance_metrics.append({
                        "name": f"{algo_name} (Quantum {quantum})",
                        "avg_waiting_time": avg_waiting_time,
                        "avg_turnaround_time": avg_turnaround_time,
                        "avg_response_time": avg_response_time
                    })
            else:  # For non-Round Robin algorithms
                for task in task_set:
                    task.reset_state() 
                algo_func()  # Run the non-Round Robin algorithm
                avg_waiting_time = sum(task.waiting_time for task in task_set) / len(task_set)
                avg_turnaround_time = sum(task.turnaround_time for task in task_set) / len(task_set)
                avg_response_time = sum(task.response_time for task in task_set) / len(task_set)

                # Store the performance metrics for non-Round Robin algorithms
                self.performance_metrics.append({
                    "name": algo_name,
                    "avg_waiting_time": avg_waiting_time,
                    "avg_turnaround_time": avg_turnaround_time,
                    "avg_response_time": avg_response_time
                })
    def plot_avg_waiting_time(self):
        """Plot Average Waiting Time comparison"""
        if hasattr(self, "current_gantt_window") and self.current_gantt_window is not None:
            plt.close(self.current_gantt_window)
            self.current_gantt_window = None

        self.close_previous_figure() 
        algorithms = [algo['name'] for algo in self.performance_metrics]
        avg_waiting_times = [algo['avg_waiting_time'] for algo in self.performance_metrics]

        self.current_figure = plt.figure() 
        bars = plt.bar(algorithms, avg_waiting_times, color='skyblue')
        plt.title("Average Waiting Time", fontsize=15, fontweight='bold')
        plt.xlabel("Algorithms", fontsize=14, fontweight='bold')
        plt.ylabel("Average Waiting Time", fontsize=14, fontweight='bold')
        plt.xticks(rotation=30, fontsize=12)

        # Add data labels on top of each bar
        for bar in bars:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
                     f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

        plt.tight_layout()
        plt.show()

    def plot_avg_turnaround_time(self):
        
        self.close_previous_figure() 
        """Plot Average Turnaround Time comparison"""
        algorithms = [algo['name'] for algo in self.performance_metrics]
        avg_turnaround_times = [algo['avg_turnaround_time'] for algo in self.performance_metrics]

        self.current_figure = plt.figure()
        bars = plt.bar(algorithms, avg_turnaround_times, color='lightgreen')
        plt.title("Average Turnaround Time", fontsize=15, fontweight='bold')
        plt.xlabel("Algorithms", fontsize=14, fontweight='bold')
        plt.ylabel("Average Turnaround Time", fontsize=14, fontweight='bold')
        plt.xticks(rotation=30, fontsize=12)

        # Add data labels on top of each bar
        for bar in bars:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
                     f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

        plt.tight_layout()
        plt.show()

    def plot_avg_response_time(self):
        """Plot Average Response Time comparison"""
        self.close_previous_figure()
        algorithms = [algo['name'] for algo in self.performance_metrics]
        avg_response_times = [algo['avg_response_time'] for algo in self.performance_metrics]

        self.current_figure = plt.figure()
        bars = plt.bar(algorithms, avg_response_times, color='orange')
        plt.title("Average Response Time", fontsize=15, fontweight='bold')
        plt.xlabel("Algorithms", fontsize=14, fontweight='bold')
        plt.ylabel("Average Response Time", fontsize=14, fontweight='bold')
        plt.xticks(rotation=30, fontsize=12)

        # Add data labels on top of each bar
        for bar in bars:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
                     f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

        plt.tight_layout()
        plt.show()

    def plot_overall_comparison(self):
        """Plot all metrics in a single figure with subplots"""
        self.close_previous_figure()
        algorithms = [algo['name'] for algo in self.performance_metrics]
        avg_waiting_times = [algo['avg_waiting_time'] for algo in self.performance_metrics]
        avg_turnaround_times = [algo['avg_turnaround_time'] for algo in self.performance_metrics]
        avg_response_times = [algo['avg_response_time'] for algo in self.performance_metrics]

        self.current_figure, axs = plt.subplots(3, 1, figsize=(6, 13))

        # Average Waiting Time
        bars = axs[0].bar(algorithms, avg_waiting_times, color='skyblue')
        axs[0].set_title("Average Waiting Time Comparison", fontsize=14, fontweight='bold')
        axs[0].set_xlabel("Algorithms", fontsize=12)
        axs[0].set_ylabel("Average Waiting Time", fontsize=12)
        axs[0].tick_params(axis='x', labelrotation=30, labelsize=10)
        axs[0].tick_params(axis='y', labelsize=10)
        for bar in bars:
            axs[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
                        f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=12)

        # Average Turnaround Time
        bars = axs[1].bar(algorithms, avg_turnaround_times, color='lightgreen')
        axs[1].set_title("Average Turnaround Time", fontsize=15, fontweight='bold')
        axs[1].set_xlabel("Algorithms", fontsize=12)
        axs[1].set_ylabel("Average Turnaround Time", fontsize=12)
        axs[1].tick_params(axis='x', labelrotation=30, labelsize=10)
        axs[1].tick_params(axis='y', labelsize=10)
        for bar in bars:
            axs[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
                        f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=12)

        # Average Response Time
        bars = axs[2].bar(algorithms, avg_response_times, color='orange')
        axs[2].set_title("Average Response Time Comparison", fontsize=14, fontweight='bold')
        axs[2].set_xlabel("Algorithms", fontsize=12)
        axs[2].set_ylabel("Average Response Time", fontsize=12)
        axs[2].tick_params(axis='x', labelrotation=30, labelsize=10)
        axs[2].tick_params(axis='y', labelsize=10)
        for bar in bars:
            axs[2].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
                        f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=12)

        # Adjust subplot spacing
        plt.subplots_adjust(hspace=1.0)
        plt.show()

    def close_previous_figure(self):
        """Close the currently open figure, if any"""
        plt.close(self.current_gantt_window)
        if self.current_figure:
            plt.close(self.current_figure)
            self.current_figure = None
    def plot_radar_chart(self):
        """Plot a radar chart to compare algorithm performance on multiple metrics."""
        self.close_previous_figure()
        # Prepare data for radar chart
        algorithms = [algo['name'] for algo in self.performance_metrics]
        metrics = ["Average Waiting Time", "Average Turnaround Time", "Average Response Time"]
        data = [
            [algo['avg_waiting_time'], algo['avg_turnaround_time'], algo['avg_response_time']]
            for algo in self.performance_metrics
        ]

        # Normalize data for fair comparison
        max_vals = np.max(data, axis=0)
        normalized_data = np.array(data) / max_vals  # Normalize by column (metric)
        
        # Radar chart setup
        num_metrics = len(metrics)
        angles = np.linspace(0, 2 * np.pi, num_metrics, endpoint=False).tolist()
        angles += angles[:1]  # Close the circle

        # Plot radar chart
        self.current_figure, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

        for algo, algo_data in zip(algorithms, normalized_data):
            algo_data = np.append(algo_data, algo_data[0])  # Close the polygon
            ax.plot(angles, algo_data, label=algo, linewidth=2)
            ax.fill(angles, algo_data, alpha=0.25)

        # Add labels for each axis
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(["20%", "40%", "60%", "80%", "100%"])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, fontsize=14, fontweight='bold')

        ax.set_title("Algorithm Performance Radar Chart", fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
        plt.tight_layout()
        plt.show()

