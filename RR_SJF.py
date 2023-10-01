import sys

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1

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

def round_robin(processes, quantum, arrival_arr, burst_arr,process_name_arr):
    num_processes = processes
    processes_info = []

    for i in range(num_processes):
        process_name = process_name_arr[i]
        arrival_time = arrival_arr[i]
        burst_time = burst_arr[i]
        processes_info.append({"job": process_name, "at": arrival_time, "bt": burst_time})
        i+=1

    time_quantum = quantum

    processes_info.sort(key=lambda x: (x["at"], x["job"]))

    solved_processes_info = []
    gantt_chart_info = []

    ready_queue = []
    current_time = processes_info[0]["at"]
    unfinished_jobs = processes_info[:]

    remaining_time = {process["job"]: process["bt"]
                      for process in processes_info}

    ready_queue.append(unfinished_jobs[0])

    first_entry_time = {}  # Dictionary to store the first entry time for each process

    print(
        f"\n{num_processes} processes\nUsing Round-Robin\nQuantum   {time_quantum}\n")
    print(f"Time   0 : {processes_info[0]['job']} arrived")

    while any(remaining_time.values()) and unfinished_jobs:
        if not ready_queue and unfinished_jobs:
            # Previously idle
            ready_queue.append(unfinished_jobs[0])
            current_time = ready_queue[0]["at"]
            print(
                f"Time  {current_time:3d} : {ready_queue[0]['job']} selected (burst {ready_queue[0]['bt']:3d})")

        process_to_execute = ready_queue[0]

        if process_to_execute["job"] not in first_entry_time:
            # Calculate and store response time when the process enters the ready queue for the first time
            first_entry_time[process_to_execute["job"]
                             ] = current_time - process_to_execute["at"]


        if remaining_time[process_to_execute["job"]] <= time_quantum:
            # Burst time less than or equal to time quantum, execute until finished
            remaining_t = remaining_time[process_to_execute["job"]]
            remaining_time[process_to_execute["job"]] -= remaining_t
            prev_current_time = current_time
            current_time += remaining_t

            gantt_chart_info.append({
                "job": process_to_execute["job"],
                "start": prev_current_time,
                "stop": current_time,
            })
            print(
                f"Time  {current_time:3d} : {process_to_execute['job']} finished")
            
        else:
            remaining_time[process_to_execute["job"]] -= time_quantum
            prev_current_time = current_time
            current_time += time_quantum

            gantt_chart_info.append({
                "job": process_to_execute["job"],
                "start": prev_current_time,
                "stop": current_time,
            })
            print(
                f"Time  {current_time:3d} : {process_to_execute['job']} selected (burst {remaining_time[process_to_execute['job']]:3d})")

        process_to_arrive_in_this_cycle = [
            p for p in processes_info if (
                p["at"] <= current_time and
                p != process_to_execute and
                p not in ready_queue and
                p in unfinished_jobs
            )
        ]

        # Push new processes to readyQueue
        ready_queue.extend(process_to_arrive_in_this_cycle)

        # Requeueing (move head/first item to tail/last)
        ready_queue.append(ready_queue.pop(0))

        # When the process finished executing
        if remaining_time[process_to_execute["job"]] == 0:
            unfinished_jobs.remove(process_to_execute)
            ready_queue.remove(process_to_execute)

            solved_processes_info.append({
                **process_to_execute,
                "ft": current_time,
                "tat": current_time - process_to_execute["at"],
                "wat": current_time - process_to_execute["at"] - process_to_execute["bt"],
                "rt": first_entry_time[process_to_execute["job"]],
            })

    # Sort the processes arrival time and then by job name
    solved_processes_info.sort(key=lambda x: (x["at"], x["job"]))

    
    # Calculate averages
    num_processes = len(solved_processes_info)
    total_tat = sum(process["tat"] for process in solved_processes_info)
    total_wat = sum(process["wat"] for process in solved_processes_info)
    total_rt = sum(process["tat"] - process["bt"]
                for process in solved_processes_info)

    print(f"Finished at time  {current_time}\n")
    print("Process   Turnaround Time   Waiting Time   Response Time")
    for process in solved_processes_info:
        print(
            f"{process['job']}   wait {process['wat']:3d} turnaround {process['tat']:3d} response {process['rt']:3d}")

    return solved_processes_info, gantt_chart_info

if len(sys.argv) != 2:
    print("Usage: python your_script.py input_filename")
    sys.exit(1)

file_path = sys.argv[1]

# Generate the output filename by replacing ".in" with ".out"
output_file = file_path.replace(".in", ".out")

processcount = 0
runfor = 0
use = ''
quantum = 0
arrival_arr = []
burst_arr = []
process_name_arr = []
processes = []

try:
    with open(file_path, 'r') as file:
        for line in file:
            line_parts = line.split("#", 1)
            line_without_comment = line_parts[0].strip()
            final_line = line_without_comment.split()
            if(final_line[0] == "processcount"):
                processcount = int(final_line[1])
            if(final_line[0] == "runfor"):
                runfor = int(final_line[1])
            if(final_line[0] == "use"):
                use = final_line[1]
            if(final_line[0] == "quantum"):
                quantum = int(final_line[1])
            if(final_line[0] == "process"):
                process_name_arr.append(final_line[2])
                arrival_arr.append(int(final_line[4]))
                burst_arr.append(int(final_line[6]))
                processes.append(Process(final_line[2], int(final_line[4]), int(final_line[6])))

except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print(f"An error occured: {str(e)}")


if(use == "rr"):
    solved_processes_info, gantt_chart_info = round_robin(processcount, quantum, arrival_arr, burst_arr, process_name_arr)


if(use == "fcfs"):
    print("fcfs code")

if(use == "sjf"):
    with open(output_file, "w") as stdout_file:
        sys.stdout = stdout_file
        print(f"{processcount} processes")
        print(f"Using preemptive Shortest Job First")
        preemptive_sjf_scheduling(runfor, processes)

    sys.stdout = sys.__stdout__
