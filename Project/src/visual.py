# visual.py

import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self):
        self.performance_metrics = []

    def run_all_algorithms(self, task_set, scheduler):
        """Run all algorithms on the same task set and collect performance data"""
        algorithms = ["FCFS", "SJF", "Priority", "RR"]  # Example list of algorithms
        self.performance_metrics = []  # To store performance data for each algorithm

        for algo in algorithms:
            scheduler.set_algorithm(algo)  # Set the current algorithm
            scheduler.run_scheduler(task_set)  # Run the scheduler with the current algorithm

            # Collect performance data
            avg_waiting_time = sum(task.waiting_time for task in task_set) / len(task_set)
            avg_turnaround_time = sum(task.turnaround_time for task in task_set) / len(task_set)
            avg_response_time = sum(task.response_time for task in task_set) / len(task_set)

            self.performance_metrics.append({
                "name": algo,
                "avg_waiting_time": avg_waiting_time,
                "avg_turnaround_time": avg_turnaround_time,
                "avg_response_time": avg_response_time
            })

    def plot_avg_waiting_time(self):
        """Plot Average Waiting Time comparison"""
        algorithms = [algo['name'] for algo in self.performance_metrics]
        avg_waiting_times = [algo['avg_waiting_time'] for algo in self.performance_metrics]

        plt.figure()
        plt.bar(algorithms, avg_waiting_times, color='skyblue')
        plt.title("Average Waiting Time Comparison")
        plt.xlabel("Algorithms")
        plt.ylabel("Average Waiting Time")
        plt.show()

    def plot_avg_turnaround_time(self):
        """Plot Average Turnaround Time comparison"""
        algorithms = [algo['name'] for algo in self.performance_metrics]
        avg_turnaround_times = [algo['avg_turnaround_time'] for algo in self.performance_metrics]

        plt.figure()
        plt.bar(algorithms, avg_turnaround_times, color='lightgreen')
        plt.title("Average Turnaround Time Comparison")
        plt.xlabel("Algorithms")
        plt.ylabel("Average Turnaround Time")
        plt.show()

    def plot_avg_response_time(self):
        """Plot Average Response Time comparison"""
        algorithms = [algo['name'] for algo in self.performance_metrics]
        avg_response_times = [algo['avg_response_time'] for algo in self.performance_metrics]

        plt.figure()
        plt.bar(algorithms, avg_response_times, color='orange')
        plt.title("Average Response Time Comparison")
        plt.xlabel("Algorithms")
        plt.ylabel("Average Response Time")
        plt.show()

    def plot_overall_comparison(self):
        """Plot all metrics in a single figure with subplots"""
        algorithms = [algo['name'] for algo in self.performance_metrics]
        avg_waiting_times = [algo['avg_waiting_time'] for algo in self.performance_metrics]
        avg_turnaround_times = [algo['avg_turnaround_time'] for algo in self.performance_metrics]
        avg_response_times = [algo['avg_response_time'] for algo in self.performance_metrics]

        fig, axs = plt.subplots(3, 1, figsize=(10, 15))

        # Average Waiting Time
        axs[0].bar(algorithms, avg_waiting_times, color='skyblue')
        axs[0].set_title("Average Waiting Time Comparison")
        axs[0].set_xlabel("Algorithms")
        axs[0].set_ylabel("Average Waiting Time")

        # Average Turnaround Time
        axs[1].bar(algorithms, avg_turnaround_times, color='lightgreen')
        axs[1].set_title("Average Turnaround Time Comparison")
        axs[1].set_xlabel("Algorithms")
        axs[1].set_ylabel("Average Turnaround Time")

        # Average Response Time
        axs[2].bar(algorithms, avg_response_times, color='orange')
        axs[2].set_title("Average Response Time Comparison")
        axs[2].set_xlabel("Algorithms")
        axs[2].set_ylabel("Average Response Time")

        plt.tight_layout()
        plt.show()
