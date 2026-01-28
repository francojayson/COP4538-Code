# import time and create a start timer
# This code measures the time taken to execute a loop of N iterations.

import time

N = 1000000

start_time = time.time()
for i in range (N):
    pass

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Loop of {N} iterations took: {elapsed_time} seconds")