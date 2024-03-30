"""
TO DO:
- Change this to work with graph in Ex1
- Discuss #4
"""

# 1. List two possible ways to implement this queue, with different efficiency (a slow one which uses linear search, and something faster) [0.2 pts]
'''
Slow Implementation using Linear Search:
In this approach, you maintain a list of unvisited vertices and iterate through the list to find the vertex with the minimum distance. 
This involves a linear search operation for each iteration, resulting in a time complexity of O(V^2) for the overall algorithm, 
where V is the number of vertices in the graph.

Faster Implementation using a Priority Queue (Heap):
Instead of using a list and linear search, you can utilize a priority queue, often implemented as a binary heap. 
This allows for efficient extraction of the vertex with the minimum distance in O(log V) time complexity. 
By using a priority queue, the overall time complexity of Dijkstra's algorithm can be reduced to O((V + E) log V), where E is the number of edges in the graph. 
This is typically much faster than the linear search approach, especially for large graphs.
'''


import time
import heapq
from graph import Graph, Vertex

class Dijkstra:
    def __init__(self, graph):
        self.graph = graph

# 2. Implement two version of the algorithm, one with the inefficient node selection logic, and one with the efficient node selection logic.
# Both should be based on the Graph class created in the course of Exercise 1. Implement the two algorithms as two methods named slowSP(node) and fastSP(node) [1 pt]
        
    def slowSP(self, source):
        distances = {vertex: float('infinity') for vertex in self.graph.vertices}
        distances[source] = 0
        unvisited = set(self.graph.vertices)

        while unvisited:
            current_vertex = None
            for vertex in unvisited:
                if current_vertex is None or distances[vertex] < distances[current_vertex]:
                    current_vertex = vertex

            unvisited.remove(current_vertex)

            for neighbor, weight in current_vertex.edges.items():
                if distances[current_vertex] + weight < distances[neighbor]:
                    distances[neighbor] = distances[current_vertex] + weight

        return distances

    def fastSP(self, source):
        distances = {vertex: float('infinity') for vertex in self.graph.vertices}
        distances[source] = 0
        pq = [(0, source)]

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            for neighbor, weight in current_vertex.edges.items():
                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(pq, (new_distance, neighbor))

        return distances

# 3. Measure the performance of each algorithm on the sample graph provided on the lab’s D2L (random.dot). [0.2 pts]
# Time the execution of the algorithm, for all nodes. Report average, max and min time
    
def measure_performance(dijkstra, nodes):
    execution_times = []
    for node in nodes:
        start_time = time.time()
        dijkstra.fastSP(node)
        end_time = time.time()
        execution_times.append(end_time - start_time)
    return execution_times


# 4. Plot a histogram of the distribution of execution times across all nodes, and discuss the results [0.1 pts]
def plot_histogram(execution_times):
    import matplotlib.pyplot as plt

    plt.hist(execution_times, bins=10)
    plt.title('Distribution of Execution Times')
    plt.xlabel('Execution Time')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == "__main__":
    # Load graph from file (assuming the file format is compatible with your Graph class)
    graph = Graph()
    graph.load_from_file("random.dot")

    dijkstra = Dijkstra(graph)

    # Nodes for performance measurement
    nodes = list(graph.vertices.values())

    # Measure performance for slowSP
    slow_execution_times = measure_performance(dijkstra, nodes)
    slow_avg_time = sum(slow_execution_times) / len(slow_execution_times)
    slow_min_time = min(slow_execution_times)
    slow_max_time = max(slow_execution_times)

    # Measure performance for fastSP
    fast_execution_times = measure_performance(dijkstra, nodes)
    fast_avg_time = sum(fast_execution_times) / len(fast_execution_times)
    fast_min_time = min(fast_execution_times)
    fast_max_time = max(fast_execution_times)

    print("Slow Algorithm:")
    print(f"Average Time: {slow_avg_time}")
    print(f"Minimum Time: {slow_min_time}")
    print(f"Maximum Time: {slow_max_time}")

    print("\nFast Algorithm:")
    print(f"Average Time: {fast_avg_time}")
    print(f"Minimum Time: {fast_min_time}")
    print(f"Maximum Time: {fast_max_time}")

    # Plot histogram
    plot_histogram(slow_execution_times)
    plot_histogram(fast_execution_times)
