import sys

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = 0

def fcfs_scheduling(processes):
    total_time = 0
    for process in processes:
        if total_time < process.arrival_time:
            total_time = process.arrival_time
        total_time += process.burst_time
        process.turnaround_time = total_time - process.arrival_time
        process.wait_time = process.turnaround_time - process.burst_time
        process.response_time = process.wait_time

def main():
    if len(sys.argv) != 3:
        print("Usage: python fcfs.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    processes = []
    process_count = 0
    total_time = 0
    algorithm = ""

    with open(input_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.split()
        if parts[0] == "process":
            name = parts[2]
            arrival_time = int(parts[4])
            burst_time = int(parts[6])
            processes.append(Process(name, arrival_time, burst_time))
            process_count += 1
        elif parts[0] == "runfor":
            total_time = int(parts[1])
        elif parts[0] == "use":
            algorithm = parts[1]

    fcfs_scheduling(processes)

    with open(output_file, 'w') as out_file:
        out_file.write(f"{process_count} processes\n")
        out_file.write(f"Using {algorithm} Scheduling\n")
        out_file.write(f"Time\t0 :")

        for time in range(total_time + 1):
            running_process = None
            for process in processes:
                if process.arrival_time <= time and process.burst_time > 0:
                    running_process = process
                    break

            if running_process:
                running_process.burst_time -= 1
                if running_process.burst_time == 0:
                    out_file.write(f" {running_process.name} finished")
                else:
                    out_file.write(f" {running_process.name} selected (burst {running_process.burst_time})")
            else:
                out_file.write(" Idle")

            if time < total_time:
                out_file.write(f"\nTime\t{time + 1} :")

        out_file.write(f"\nFinished at time {total_time}\n\n")

        for process in processes:
            out_file.write(f"{process.name} wait   {process.wait_time} turnaround   {process.turnaround_time} response {process.response_time}\n")

if __name__ == "__main__":
    main()
