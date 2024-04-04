# Importing necessary libraries
import heapq
import matplotlib.pyplot as plt
from time import time

# Definition of a graph node
class GraphNode:
    # Initialize a graph node with data
    def __init__(self, data):
        self.data = data  # Node's data
        self.edges = {}   # Dictionary to store edges and weights

    # Representation of a graph node
    def __repr__(self):
        return f"GraphNode({self.data})"

# Definition of a graph
class Graph:
    # Initialize a graph
    def __init__(self):
        self.nodes = {}  # Dictionary to store nodes and their edges

    # Add a node to the graph
    def add_node(self, data):
        # Check if node already exists
        for node in self.nodes:
            if node.data == data:
                return node
        # Create a new node if it doesn't exist
        new_node = GraphNode(data)
        self.nodes[new_node] = new_node.edges
        return new_node

    # Add an edge between two nodes
    def add_edge(self, n1, n2, weight=1):
        # Ensure both nodes exist in the graph
        if n1 in self.nodes and n2 in self.nodes:
            # Add edge with weight in both directions
            self.nodes[n1][n2] = weight
            self.nodes[n2][n1] = weight

# Extending the Graph class for Dijkstra's algorithm
class DijkstraGraph(Graph):
    # Slow shortest path implementation
    def slowSP(self, start_node):
        # Initialize distances from start node to infinity
        distances = {node: float('inf') for node in self.nodes}
        distances[start_node] = 0  # Distance to start node is 0
        unvisited = set(self.nodes)  # Set of unvisited nodes

        # Loop until all nodes are visited
        while unvisited:
            # Select the unvisited node with the minimum distance
            current_node = min(unvisited, key=lambda node: distances[node])
            unvisited.remove(current_node)  # Mark as visited

            # Update distances for neighbors
            for neighbor, weight in self.nodes[current_node].items():
                new_distance = distances[current_node] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

        return distances

    # Fast shortest path implementation using a priority queue
    def fastSP(self, start_node):
        # Initialize distances from start node to infinity
        distances = {node: float('inf') for node in self.nodes}
        distances[start_node] = 0  # Distance to start node is 0
        priority_queue = [(0, start_node)]  # Priority queue for nodes to visit

        # Loop until priority queue is empty
        while priority_queue:
            # Pop the node with the minimum distance
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_distance > distances[current_node]:
                continue  # Skip if we've found a better path

            # Update distances for neighbors
            for neighbor, weight in self.nodes[current_node].items():
                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        return distances

# Measure the execution time of a method
def measure_performance(graph, start_node, method):
    start_time = time()  # Start timer
    # Execute the selected method
    if method == 'slow':
        graph.slowSP(start_node)
    elif method == 'fast':
        graph.fastSP(start_node)
    end_time = time()  # End timer
    return end_time - start_time  # Return execution time

# Collect performance data over all nodes
def performance_over_nodes(graph, method):
    times = []  # List to store execution times
    # Measure performance for each node
    for node in graph.nodes:
        times.append(measure_performance(graph, node, method))
    return times  # Return list of times

# Plot histogram of execution times
def plot_histogram(slow_times, fast_times):
    # Plot histograms for both methods
    plt.hist(slow_times, bins=10, alpha=0.5, label='SlowSP')
    plt.hist(fast_times, bins=10, alpha=0.5, label='FastSP')
    plt.title('Distribution of Execution Times')  # Title
    plt.xlabel('Execution Time (s)')  # X-axis label
    plt.ylabel('Frequency')  # Y-axis label
    plt.legend(loc='upper right')  # Legend
    plt.show()  # Display plot
