# Dijkstra Graph
DijkstraGraph = {
    "A": [("B", 15), ("D", 12), ("L", 10)],
    "B": [("A", 15), ("C", 1), ("L", 8)],
    "C": [("B", 1), ("D", 10), ("E", 17), ("F", 25)],
    "D": [("A", 12), ("C", 10), ("I", 22)],
    "E": [("C", 17), ("F", 30), ("L", 18), ("M", 18)],
    "F": [("C", 25), ("E", 30), ("G", 13), ("M", 35)],
    "G": [("F", 13), ("H", 40), ("K", 15), ("N", 5)],
    "H": [("G", 40), ("I", 12), ("J", 23)],
    "I": [("D", 22), ("H", 12)],
    "J": [("H", 23), ("K", 14)],
    "K": [("G", 15), ("J", 14)],
    "L": [("A", 10), ("B", 8), ("E", 18), ("M", 18)],
    "M": [("E", 18), ("F", 35), ("L", 18), ("N", 9)],
    "N": [("G", 5), ("M", 9)],
}

# For second weighted graph, use the Dijkstra algorithm to create Python 
# code find the cheapest path from node A to node K.
# For each step print out which node you are selecting and its cost.
# Print out the cheapest path from node A to node K.
# Print out the total cost of taking this path from node A to node K.

def dijkstra(graph, start, goal):
    import heapq

    # Priority queue to store (cost, vertex) pairs
    queue = [(0, start)]
    # Dictionary to store the minimum cost to reach each vertex
    min_cost = {vertex: float('inf') for vertex in graph}
    min_cost[start] = 0
    # Dictionary to store the parent of each vertex for path reconstruction
    parent = {start: None}

    while queue:
        current_cost, current_vertex = heapq.heappop(queue)

        # If we reached the goal, reconstruct the path
        if current_vertex == goal:
            path = []
            while current_vertex is not None:
                path.append(current_vertex)
                current_vertex = parent[current_vertex]
            path.reverse()
            print("Cheapest path:", " -> ".join(path))
            print("Total cost:", current_cost)
            return

        # Explore neighbors
        for neighbor, weight in graph[current_vertex]:
            new_cost = current_cost + weight
            if new_cost < min_cost[neighbor]:
                min_cost[neighbor] = new_cost
                parent[neighbor] = current_vertex
                heapq.heappush(queue, (new_cost, neighbor))
                print(f"Selecting node {neighbor} with cost {new_cost} from node {current_vertex}")

    print(f"No path found from {start} to {goal}.")

print("Dijkstra's shortest path from A to K:")
dijkstra(DijkstraGraph, "A", "K")


