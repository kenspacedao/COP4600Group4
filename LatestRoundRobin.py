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

processcount = 0
runfor = 0
use = ''
quantum = 0
arrival_arr = []
burst_arr = []
process_name_arr = []

file_path = "c10-rr.in"
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

except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print(f"An error occured: {str(e)}")


if(use == "rr"):
    solved_processes_info, gantt_chart_info = round_robin(processcount, quantum, arrival_arr, burst_arr, process_name_arr)


if(use == "fcfs"):
    print("fcfs code")

if(use == "sjf"):
    print("sjf code")
