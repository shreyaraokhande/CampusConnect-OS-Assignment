# CampusConnect Operating Systems Assignment (Part 4)

## Programming Language

Python 3

Repository Contents:

- scheduler.py
- synchronization.py
- README.md

---

# 1. Scheduling Simulator

The scheduling simulator implements the following CPU scheduling algorithms:

- First Come First Serve (FCFS)
- Shortest Job First (SJF – Non-Preemptive)
- Round Robin (Configurable Time Quantum)

### Input Dataset

| Process | Arrival Time | Burst Time |
|---------|--------------|-----------:|
| P1 | 0 | 6 |
| P2 | 2 | 4 |
| P3 | 4 | 2 |
| P4 | 6 | 5 |
| P5 | 8 | 3 |

### Tie-Breaking Rules

- If two or more processes have the same arrival time, the process appearing first in the input list is scheduled first.
- For SJF, if two processes have the same burst time, arrival time is considered first, followed by the original process order.
- In Round Robin, any process that arrives during the current quantum is added to the ready queue before the preempted process is reinserted at the back of the queue.

The scheduler prints:

- Waiting Time for each process
- Turnaround Time for each process
- Average Waiting Time
- Average Turnaround Time

---

# 2. Priority Scheduling with Aging

### Assumption

To demonstrate true starvation, new high-priority processes continue arriving at fixed intervals. Without this assumption, every process in a finite set would eventually execute.

Higher numeric value indicates **higher priority**.

### Initial Priorities

| Process | Priority |
|----------|---------:|
| P1 | 10 |
| P2 | 9 |
| P3 | 8 |
| P4 | 7 |
| P5 | 2 |

Without aging, P5 continues waiting because newly arriving high-priority processes keep entering the ready queue with priorities higher than 2.

### Aging Policy

Every **5 time units**, a waiting process gains **+1 priority**.

### Aging Trace

| Time | P5 Priority | Event |
|------|------------:|-------|
| 0 | 2 | P5 enters ready queue |
| 5 | 3 | Waiting for first interval |
| 10 | 4 | Priority increased |
| 15 | 5 | Priority increased |
| 20 | 6 | Priority increased |
| 25 | 7 | Eventually reaches runnable priority |

Without aging, P5 would continue waiting indefinitely because new higher-priority jobs keep arriving.

With aging, its priority gradually increases until it is eventually selected for execution, preventing starvation.

---

# 3. Synchronization

The synchronization program demonstrates two scenarios.

## Unsynchronized Version

- Two threads increment a shared counter.
- A `threading.Barrier` is placed between the read and write operations.
- Both threads read the same stale counter value before either writes.
- Exactly one increment is lost every run, producing an incorrect counter value.

## Synchronized Version

A binary semaphore (`threading.Lock`) protects the critical section.

The Barrier is removed from this version because keeping it inside the locked critical section could itself create a deadlock.

The final counter value always matches the expected value.

---

# 4. Deadlock Analysis

### Scenario

Three backend processes:

- P1 – Assignment Service
- P2 – Enrollment Service
- P3 – Notification Service

Three resources:

- R1 – Database Connection
- R2 – File Lock
- R3 – Cache Lock

### Four Necessary Conditions

**Mutual Exclusion**

Each resource can be used by only one process at a time.

**Hold and Wait**

Each process holds one resource while requesting another resource.

**No Preemption**

Resources cannot be forcibly taken away until the owning process releases them.

**Circular Wait**

Each process waits for a resource currently held by another process, forming a cycle.

### Resource Allocation Graph (Text Form)

- R1 → P1 (allocated)
- P1 → R2 (requested)
- R2 → P2 (allocated)
- P2 → R3 (requested)
- R3 → P3 (allocated)
- P3 → R1 (requested)

This creates the cycle:

P1 → R2 → P2 → R3 → P3 → R1 → P1

### Edge to Remove

Remove:

**P3 → R1 (requested)**

Removing this request breaks the circular wait and prevents the deadlock.

### Deadlock Prevention Strategy

**Resource Ordering**

All processes must request resources in the same predefined order (for example R1 → R2 → R3).

### Limitation

A strict ordering may reduce flexibility and can increase waiting time when processes require resources in different sequences.

---

# Conclusion

This assignment demonstrates CPU scheduling, starvation prevention using aging, synchronization using binary semaphores, deterministic race-condition detection using a Barrier, and deadlock analysis using a resource allocation graph. The implementation satisfies the required scheduling algorithms and synchronization techniques while explaining practical operating system concepts used in the CampusConnect backend.
