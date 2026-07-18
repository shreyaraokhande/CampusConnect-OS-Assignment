"""
CampusConnect Operating Systems Assignment
Part 4 - Synchronization Demo

This program demonstrates:

1. An unsynchronized race condition using threading.Barrier
   (guaranteed incorrect result)

2. A synchronized version using a binary semaphore (Lock)
   without using the Barrier.

Author: Shreya Raokhande
"""

import threading

# ==========================================================
# PART 1 - UNSYNCHRONIZED VERSION
# ==========================================================

counter = 0

# Barrier forces both threads to read the same stale value
barrier = threading.Barrier(2)


def unsafe_increment():

    global counter

    # Both threads read BEFORE either writes
    temp = counter

    # Wait until both threads have finished reading
    barrier.wait()

    # Both compute from the same stale value
    temp = temp + 1

    # Both write back
    counter = temp


print("=" * 60)
print("UNSYNCHRONIZED VERSION")
print("=" * 60)

counter = 0

t1 = threading.Thread(target=unsafe_increment)
t2 = threading.Thread(target=unsafe_increment)

t1.start()
t2.start()

t1.join()
t2.join()

print("Expected Counter Value : 2")
print("Actual Counter Value   :", counter)

if counter != 2:
    print("Race Condition Successfully Demonstrated.")
else:
    print("Unexpected Result")


# ==========================================================
# PART 2 - SYNCHRONIZED VERSION
# ==========================================================

print("\n")
print("=" * 60)
print("SYNCHRONIZED VERSION (Binary Semaphore / Lock)")
print("=" * 60)

counter = 0

lock = threading.Lock()


def safe_increment():

    global counter

    # Critical section
    with lock:
        temp = counter
        temp = temp + 1
        counter = temp


t3 = threading.Thread(target=safe_increment)
t4 = threading.Thread(target=safe_increment)

t3.start()
t4.start()

t3.join()
t4.join()

print("Expected Counter Value : 2")
print("Actual Counter Value   :", counter)

if counter == 2:
    print("Synchronization Successful.")
else:
    print("Synchronization Failed.")
