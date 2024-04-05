 # 1. List two possible ways to implement this queue, with different efficiency  
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
import heapq
import matplotlib.pyplot as plt
from time import time

### AI declaration: 
# Used it to help with debugging the code file. As well as helping 
# to further understand what some of the points in the quesiion were asking for. 

# Definition of a graph node
class GraphNode:
    # Initialize a graph node with data
    def __init__(self, data):
        self.data = data   
        self.edges = {}    
    # Representation of a graph node
    def __repr__(self):
        return f"GraphNode({self.data})"

# Definition of a graph
class Graph:
    # Initialize a graph
    def __init__(self):
        self.nodes = {}  # Dictionary to store nodes and their edges

    # Add a node to the graph
    def addNode(self, data):
        # Check if node already exists
        for node in self.nodes:
            if node.data == data:
                return node
        # Create a new node if it doesn't exist
        new_node = GraphNode(data)
        self.nodes[new_node] = new_node.edges
        return new_node

    # Add an edge between two nodes
    def addEdge(self, n1, n2, weight=1):
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
        distances[start_node] = 0   
        unvisited = set(self.nodes)  
        # Loop until all nodes are visited
        while unvisited:
            # Select the unvisited node with the minimum distance
            current_node = min(unvisited, key=lambda node: distances[node])
            unvisited.remove(current_node)   

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
        distances[start_node] = 0   
        priority_queue = [(0, start_node)]   

        # Loop until priority queue is empty
        while priority_queue:
            # Pop the node with the minimum distance
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_distance > distances[current_node]:
                continue   

            # Update distances for neighbors
            for neighbor, weight in self.nodes[current_node].items():
                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        return distances

# Measure the execution time of a method
def measurePerformance(graph, start_node, method):
    start_time = time()   
    # Execute the selected method
    if method == 'slow':
        graph.slowSP(start_node)
    elif method == 'fast':
        graph.fastSP(start_node)
    end_time = time()  
    return end_time - start_time  

# Collect performance data over all nodes
def performanceOverNodes(graph, method):
     # List to store execution times
    times = [] 
    # Measure performance for each node
    for node in graph.nodes:
        times.append(measurePerformance(graph, node, method))
    return times  

# Plot histogram of execution times
def plot_histogram(slow_times, fast_times):
    # Plot histograms for both methods
    plt.hist(slow_times, bins=10, alpha=0.5, label='SlowSP')
    plt.hist(fast_times, bins=10, alpha=0.5, label='FastSP')
    plt.title('Distribution of Execution Times')  
    plt.xlabel('Execution Time (s)')  
    plt.ylabel('Frequency')   
    plt.legend(loc='upper right')   
    plt.show()   

'''
The FastSP method surpasses the slowSP in efficiency with a priority queue to adeptly identify the node 
with the lowest distance. 
'''
