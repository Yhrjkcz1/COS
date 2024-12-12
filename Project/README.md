# COS
# CPU Scheduling Simulator

## Project Overview
**CPU Scheduling Simulator** is a tool designed to simulate classic CPU scheduling algorithms, providing users with an intuitive way to understand and compare the performance of various algorithms. The program uses a dynamic Gantt chart and performance metrics to visualize the scheduling process and its results.

---

## Features

- **Supported Scheduling Algorithms**:
  1. **FCFS (First-Come, First-Served)**
  2. **Non-Preemptive SJF (Shortest Job First)**
  3. **Preemptive SJF (Shortest Remaining Time First)**
  4. **Priority Scheduling**
  5. **Round Robin (RR)**

- **Key Functionalities**:
  - **Manual or Random Process Generation**:
    - Input `Process ID`, `Arrival Time`, `Burst Time`, and `Priority`.
    - Generate random process data with one click.
  - **Simulation and Algorithm Comparison**:
    - Select an algorithm and run the simulation to visualize the scheduling process with a dynamic Gantt chart.
    - Automatically calculate and display performance metrics (average waiting time, turnaround time, response time, and context switches).
  - **Algorithm Analysis**:
    - Graphically compare the performance of different algorithms, including metrics such as waiting time, turnaround time, and response time.

---

## Usage Instructions

1. **Installation**:
   - Clone or download the project repository to your local machine.
   - Ensure you have Python 3.8 or higher installed along with the required libraries (see System Requirements).

2. **Run the GUI**:
   - Navigate to the project directory in your terminal or command prompt.
   - Execute the following command to launch the GUI:
     ```bash
     python GUI.py
     ```

3. **Add Processes**:
   - Input process details, including `Process ID`, `Arrival Time`, `Burst Time`, and (optional) `Priority`.
   - Click the `Add Process` button to add the process to the queue.

4. **Select Scheduling Algorithm**:
   - Use the `Choose Algorithm` dropdown menu to select an algorithm (e.g., FCFS, Non-Preemptive SJF, etc.).

5. **Run Simulation**:
   - For Round Robin, set the time quantum. Then click the `Run Simulation` button to start the simulation.

6. **View Results**:
   - The dynamic Gantt chart visualizes the scheduling process, and performance metrics are displayed on the right panel.

7. **Reset or Reload Data**:
   - Use the `Reset` button to clear all data or the `Reload` button to restore the previous process queue.

---

## GUI Overview

- **Top Control Panel**:
  - The `Add Process` button is used to add processes.
  - `Random Generate` creates random process data.
  - `Run Simulation` runs the selected scheduling algorithm.
  - `Reset` and `Reload` buttons clear or restore process data.

- **Middle Display Area**:
  - **Gantt Chart** dynamically visualizes the scheduling process.

- **Right Performance Panel**:
  - Displays performance metrics, including average waiting time, turnaround time, response time, and context switches.
  - Provides graphical comparisons of algorithm performance for multi-dimensional analysis.

---

## System Requirements

- **Python Version**: Python 3.8 or higher  

- **Required Libraries**:  
  1. **`tkinter`**: For building the graphical user interface (GUI).  
  2. **`ttk` and `messagebox`**: Extensions for tkinter to enhance the interface.  
  3. **`matplotlib`**: For creating and animating Gantt charts, as well as other visualizations.  
     - Submodules used:  
       - `matplotlib.pyplot`: For plotting graphs.  
       - `matplotlib.animation.FuncAnimation`: For creating dynamic animations.  
       - `matplotlib.backends.backend_tkagg`: For embedding matplotlib visualizations in the GUI.  
  4. **`numpy`**: For numerical calculations and data manipulation.  
  5. **`random`**: For generating random process data.  
  6. **`copy`**: For duplicating process objects during scheduling operations.  
  7. **Custom Modules**:  
     - `scheduler`: Implements the scheduling logic and algorithms.  
     - `process`: Defines the structure and attributes of processes.  
     - `visual`: Manages visualization and animations.  

### Install Required Libraries

Run the following command to install all necessary libraries:
```bash
pip install matplotlib numpy
```

