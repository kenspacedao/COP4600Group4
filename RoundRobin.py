class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_burst = burst
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = -1

def round_robin(processes, time_slice):
    queue = []  # Process queue
    current_time = 0  # Current time
    completed_processes = []

    while processes or queue:
        # Add arriving processes to the queue
        for process in processes:
            if process.arrival <= current_time:
                queue.append(process)
                processes.remove(process)

        if not queue:
            # No processes in the queue, but more processes are yet to arrive
            current_time += 1
            continue

        # Get the first process in the queue
        current_process = queue.pop(0)

        if current_process.response_time == -1:
            current_process.response_time = current_time - current_process.arrival

        # Execute the process for its time slice or remaining burst time, whichever is smaller
        if current_process.remaining_burst <= time_slice:
            current_time += current_process.remaining_burst
            current_process.remaining_burst = 0
            current_process.turnaround_time = current_time - current_process.arrival
            current_process.waiting_time = current_process.turnaround_time - current_process.burst
            completed_processes.append(current_process)
        else:
            current_time += time_slice
            current_process.remaining_burst -= time_slice
            queue.append(current_process)

    return completed_processes

def calculate_metrics(processes):
    total_turnaround_time = 0
    total_waiting_time = 0
    total_response_time = 0

    for process in processes:
        total_turnaround_time += process.turnaround_time
        total_waiting_time += process.waiting_time
        total_response_time += process.response_time

    avg_turnaround_time = total_turnaround_time / len(processes)
    avg_waiting_time = total_waiting_time / len(processes)
    avg_response_time = total_response_time / len(processes)

    return avg_turnaround_time, avg_waiting_time, avg_response_time

# Example usage
if __name__ == "__main__":
    p1 = Process("P1", 0, 10)
    p2 = Process("P2", 1, 5)
    p3 = Process("P3", 3, 8)

    processes = [p1, p2, p3]
    time_slice = 2

    completed_processes = round_robin(processes, time_slice)

    avg_turnaround_time, avg_waiting_time, avg_response_time = calculate_metrics(completed_processes)

    print("Process\tTurnaround Time\tWaiting Time\tResponse Time")
    for process in completed_processes:
        print(f"{process.name}\t{process.turnaround_time}\t\t{process.waiting_time}\t\t{process.response_time}")

    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print(f"Average Waiting Time: {avg_waiting_time}")
    print(f"Average Response Time: {avg_response_time}")
