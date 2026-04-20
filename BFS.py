from collections import deque # Import the deque class from the collections module to use as a queue for BFS

# BFS Graph
BFSGraph = {
"A": ["B", "D", "L"],
"B": ["A", "C", "L"],
"C": ["B", "E", "F", "D"],
"D": ["A", "C", "I"],
"E": ["L", "C", "F", "M"],
"F": ["C", "E", "G", "M"],
"G": ["F", "K", "N"],
"H": ["I", "J", "G"],
"I": ["D", "H"],
"J": ["H", "K"],
"K": ["G", "J"],
"L": ["A", "B", "E", "M"],
"M": ["L", "E", "F", "N"],
"N": ["M", "G"],
} 

def bfs(graph, start, goal):
    visited = set([start]) # Initialize visited set with the starting vertex
    queue = deque([start]) # Initialize queue with the starting vertex
    parent = {start: None} # Dictionary to track the parent of each vertex for path reconstruction

    while queue: # While there are vertices to explore
        current = queue.popleft() # Dequeue the next vertex to explore
        discovered_this_step = [] # List to track newly discovered vertices in this step
            
        for neighbor in graph[current]: # Iterate through the neighbors of the current vertex
            if neighbor not in visited: # If the neighbor has not been visited
                visited.add(neighbor)   # Mark the neighbor as visited
                parent[neighbor] = current # Set the parent of the neighbor to the current vertex
                queue.append(neighbor)     # Enqueue the neighbor for future exploration
                discovered_this_step.append(neighbor) # Add the newly discovered neighbor to the list for this step

        if discovered_this_step: # Only print if there are newly discovered vertices
            print(f"From {current}, newly discovered vertices: {discovered_this_step}") # Print the newly discovered vertices from the current vertex

        if current == goal: # If the goal vertex is reached,
            break           # Exit the loop to reconstruct the path

    if goal not in parent:  # If the goal vertex was never reached, print a message and return
        print(f"No path found from {start} to {goal}.") # Print a message indicating that no path was found
        return # Exit the function if no path is found
    
    path = []   # Reconstruct the path from the goal back to the start using the parent dictionary
    node = goal # Start with the goal vertex
    while node is not None: # While there are still nodes to trace back (until we reach the start vertex which has a parent of None)
        path.append(node)   # Add the current node to the path
        node = parent[node] # Move to the parent of the current node to continue tracing back the path
    path.reverse()          # Reverse the path to get the correct order from start to goal

    print("Final shortest path:", " -> ".join(path)) # Print the final shortest path from start to goal

print("BFS shortest path from A to K:") # Print a header for the BFS shortest path from vertex A to vertex K
bfs(BFSGraph, "A", "K")                 # Call the bfs function with the BFSGraph, starting vertex "A", and goal vertex "K" to find and print the shortest path from A to K using BFS.
