"""
CampusConnect Operating Systems Assignment
Part 4 - CPU Scheduling Simulation

Algorithms Implemented
1. First Come First Serve (FCFS)
2. Shortest Job First (Non-Preemptive)
3. Round Robin (Configurable Quantum)

Tie Breaking Rules

1. If two processes arrive together,
   process appearing first in input executes first.

2. SJF
   If burst times are equal,
   earlier arrival executes first.
   If arrival is also equal,
   process ID is used.

3. Round Robin
   When quantum expires,
   newly arrived processes are added to the queue
   BEFORE re-adding the running process.

Author: Shreya Raokhande
"""

from collections import deque
import copy


class Process:

    def __init__(self, pid, arrival, burst):

        self.pid = pid
        self.arrival = arrival
        self.burst = burst

        self.remaining = burst

        self.waiting = 0
        self.turnaround = 0
        self.completion = 0

        self.order = 0


############################################################
# Utility Function
############################################################

def print_results(title, process_list):

    print("\n")
    print("=" * 65)
    print(title)
    print("=" * 65)

    print(
        "{:<8}{:<10}{:<10}{:<12}{:<15}".format(
            "PID",
            "Arrival",
            "Burst",
            "Waiting",
            "Turnaround"
        )
    )

    total_wait = 0
    total_turn = 0

    for p in process_list:

        total_wait += p.waiting
        total_turn += p.turnaround

        print(
            "{:<8}{:<10}{:<10}{:<12}{:<15}".format(
                p.pid,
                p.arrival,
                p.burst,
                p.waiting,
                p.turnaround
            )
        )

    n = len(process_list)

    print("-" * 65)

    print(
        "Average Waiting Time      : {:.2f}".format(
            total_wait / n
        )
    )

    print(
        "Average Turnaround Time   : {:.2f}".format(
            total_turn / n
        )
    )


############################################################
# FCFS Scheduling
############################################################

def fcfs(processes):

    plist = copy.deepcopy(processes)

    plist.sort(
        key=lambda x: (
            x.arrival,
            x.order
        )
    )

    current_time = 0

    for p in plist:

        if current_time < p.arrival:
            current_time = p.arrival

        p.waiting = current_time - p.arrival

        current_time += p.burst

        p.completion = current_time

        p.turnaround = (
            p.completion - p.arrival
        )

    print_results(
        "FIRST COME FIRST SERVE",
        plist
    )
  ############################################################
# SJF (Non-Preemptive)
############################################################

def sjf(processes):

    plist = copy.deepcopy(processes)

    completed = 0
    n = len(plist)

    current_time = 0

    visited = [False] * n

    while completed < n:

        ready = []

        for i, p in enumerate(plist):

            if (not visited[i]) and p.arrival <= current_time:
                ready.append((p.burst, p.arrival, p.order, i))

        if not ready:

            current_time += 1
            continue

        ready.sort()

        index = ready[0][3]

        p = plist[index]

        p.waiting = current_time - p.arrival

        current_time += p.burst

        p.completion = current_time

        p.turnaround = p.completion - p.arrival

        visited[index] = True

        completed += 1

    print_results(
        "SHORTEST JOB FIRST (NON-PREEMPTIVE)",
        plist
    )


############################################################
# Round Robin
############################################################

def round_robin(processes, quantum):

    plist = copy.deepcopy(processes)

    plist.sort(
        key=lambda x: (
            x.arrival,
            x.order
        )
    )

    queue = deque()

    current_time = 0
    completed = 0
    n = len(plist)

    visited = [False] * n

    while completed < n:

        # Add newly arrived processes
        for i, p in enumerate(plist):

            if (
                not visited[i]
                and p.arrival <= current_time
            ):

                queue.append(i)
                visited[i] = True

        if not queue:

            current_time += 1
            continue

        index = queue.popleft()

        p = plist[index]

        execute = min(
            quantum,
            p.remaining
        )

        start_time = current_time

        current_time += execute

        p.remaining -= execute

        # IMPORTANT:
        # Add processes that arrived during the quantum
        # BEFORE re-adding the running process.

        for i, process in enumerate(plist):

            if (
                not visited[i]
                and process.arrival <= current_time
            ):

                queue.append(i)
                visited[i] = True

        if p.remaining > 0:

            queue.append(index)

        else:

            completed += 1

            p.completion = current_time

            p.turnaround = (
                p.completion - p.arrival
            )

            p.waiting = (
                p.turnaround - p.burst
            )

    print_results(
        f"ROUND ROBIN (Quantum = {quantum})",
        plist
    )
  ############################################################
# Sample Dataset (5 Processes)
############################################################

processes = [

    Process("P1", 0, 6),
    Process("P2", 2, 4),
    Process("P3", 4, 2),
    Process("P4", 6, 5),
    Process("P5", 8, 3)

]

# Store definition order for deterministic tie-breaking
for index, process in enumerate(processes):
    process.order = index


############################################################
# Main Program
############################################################

def main():

    print("\nCampusConnect CPU Scheduling Simulation")
    print("=" * 65)

    fcfs(processes)

    sjf(processes)

    quantum = 2

    round_robin(processes, quantum)


if __name__ == "__main__":
    main()
