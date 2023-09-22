import sys

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1

def parse_input_file(filename):
    processes = []
    total_time = 0

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        process_count = None
        i = 0  # Initialize an index variable

        while i < len(lines):
            line = lines[i].strip()

            # Split line at '#' to remove comments
            line_parts = line.split("#", 1)
            line = line_parts[0].strip()  # Get the part before the comment

            if line.startswith("processcount"):
                process_count = int(line.split()[1])
            elif line.startswith("runfor"):
                total_time = int(line.split()[1])
            elif line.startswith("process name") and process_count:
                parts = line.split()
                if len(parts) == 7:  # Check if the line has the expected format
                    process_name = parts[2]
                    arrival_time = int(parts[4])

                    # Check if there are enough lines for process details
                    if i + 1 < len(lines):
                        burst_time = int(lines[i].strip().split()[6])
                        processes.append(Process(process_name, arrival_time, burst_time))
                        process_count -= 1
                    else:
                        print("Error: Incomplete process details in the input file.")
                        sys.exit(1)
                else:
                    print("Error: Invalid format for process details.")
                    sys.exit(1)
            elif line.startswith("end") and process_count == 0:
                break

            i += 1

    except Exception as e:
        print(f"Error: Could not parse the input file due to invalid input. {e}")
        sys.exit(1)

    return total_time, processes

def preemptive_sjf_scheduling(total_time, processes):
    current_time = 0
    completed_processes = []
    previous_process = None

    for current_time in range(total_time):
        eligible_processes = [p for p in processes if p.arrival_time <= current_time]
        if not eligible_processes:
            print(f"Time {current_time} : Idle")
            continue

        for p in processes:
            if p.arrival_time == current_time:
                print(f"Time {current_time} : {p.name} arrived")


        shortest_process = min(eligible_processes, key=lambda p: p.burst_time)

        if shortest_process.response_time == -1:
            shortest_process.response_time = current_time - shortest_process.arrival_time

        if previous_process is None or (shortest_process != previous_process and shortest_process.burst_time < previous_process.burst_time):
            if shortest_process.response_time == -1:
                shortest_process.response_time = current_time - shortest_process.arrival_time
            print(f"Time {current_time} : {shortest_process.name} selected (burst {shortest_process.burst_time})")

        # Update wait time for other processes
        for p in processes:
            if p != shortest_process and p.arrival_time <= current_time:
                p.wait_time += 1

        shortest_process.burst_time -= 1

        if shortest_process.burst_time <= 0:
            completed_processes.append(shortest_process)
            processes.remove(shortest_process)
            shortest_process.turnaround_time = current_time + 1 - shortest_process.arrival_time
            print(f"Time {current_time + 1} : {shortest_process.name} finished")
            shortest_process = None

        previous_process = shortest_process

    print(f"Finished at time  {total_time}")

    # Check if any processes are still running
    unfinished_processes = [p for p in processes if p.burst_time > 0]

    if unfinished_processes:
        print("Processes that did not finish:")
        for p in unfinished_processes:
            print(f"{p.name} (burst {p.burst_time})")

    print("\nExecution Order:")
    for p in completed_processes:
        print(f"{p.name} ", end="")
    print("\n")

    print("Process\tResponse Time\tWait Time\tTurnaround Time")
    for p in completed_processes:
        print(f"{p.name}\t{p.response_time}\t\t{p.wait_time}\t\t{p.turnaround_time}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py input_filename")
        sys.exit(1)

    input_file = sys.argv[1]

    # Generate the output filename by replacing ".in" with ".out"
    output_file = input_file.replace(".in", ".out")

    total_time, processes = parse_input_file(input_file)

    # Redirect the standard output to the output file
    with open(output_file, "w") as stdout_file:
        sys.stdout = stdout_file

        print("Preemptive SJF Scheduling:")
        preemptive_sjf_scheduling(total_time, processes)

    # Reset the standard output back to the console
    sys.stdout = sys.__stdout__

    print(f"Output written to {output_file}")
