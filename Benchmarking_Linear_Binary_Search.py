import random
import time

# Generate a list of 100 dummy contacts.
# Each contact should be a dictionary with 'first name' and 'last name'.
# The list must be sorted by 'last name' from 1 to 100.
contacts = []
for i in range(1, 101):
    contact = {
        "first name": f"First {i}",
        "last name": f"Last {i}"
    }
    contacts.append(contact)

# Sort the list by 'last name'
contacts.sort(key=lambda x: x["last name"])

# Linear Search (Old Method)
def linear_search(arr, target_last):
    for i in range(len(arr)):
        if arr[i]["last name"] == target_last:
            return arr[i]
    return -1

# Binary Search (New Method)
def binary_search(arr, target_last):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid]["last name"] == target_last:
            return arr[mid]
        elif arr[mid]["last name"] < target_last:
            low = mid + 1
        else:
            high = mid - 1
    
    return -1

# Benchmarking the two search methods
def benchmark_search():
    target = random.choice(contacts)["last name"]  # Randomly select a target last name from the contacts

    # Benchmark Linear Search
    start_time = time.perf_counter()

    for _ in range(1000):  # Run the search 1000 times to get an average time
        linear_search(contacts, target)

    linear_time = time.perf_counter() - start_time

    # Benchmark Binary Search
    start_time = time.perf_counter()

    for _ in range(1000):  # Run the search 1000 times to get an average time
        binary_search(contacts, target)

    binary_time = time.perf_counter() - start_time

    print(f"Linear Search Time: {linear_time}")
    print(f"Binary Search Time: {binary_time}")

    # Calculate how much faster the binary search is compared to the linear search
    if linear_time > 0:
        speedup = linear_time / binary_time
        print(f"Binary search is {speedup:.2f} times faster than linear search.") 

benchmark_search()
