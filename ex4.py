# AI WAS USED IN THIS EXERCISE
import timeit

class GraphNode:
    def __init__(self, data):
        self.data = data


# 1. Starting from the Graph class created in Exercise 1, create a Graph2 class which uses (you guessed it) an adjacency matrix to keep track of the edges [0.9 pts]
    # Each location in the matrix must be 0 if an edge is not present, and W (where W is the edge’s weight) if an edge is present

class Graph2:
    def __init__(self):
        self.adjacency_matrix = {}

    # Add a node to the adjacency matrix.
    def add_node(self, data):
        if data not in self.adjacency_matrix:
            self.adjacency_matrix[data] = {}
            return GraphNode(data)
        return None

    # Remove a node from the adjacency matrix.
    def remove_node(self, node):
        if node.data in self.adjacency_matrix:
            del self.adjacency_matrix[node.data]
            for key in self.adjacency_matrix:
                if node.data in self.adjacency_matrix[key]:
                    del self.adjacency_matrix[key][node.data]

    # Add an edge to the adjacency matrix.
    def add_edge(self, n1, n2, weight=1):
        if n1.data in self.adjacency_matrix and n2.data in self.adjacency_matrix:
            self.adjacency_matrix[n1.data][n2.data] = weight
            self.adjacency_matrix[n2.data][n1.data] = weight

    # Remove an edge from the adjacency matrix.
    def remove_edge(self, n1, n2):
        if n1.data in self.adjacency_matrix and n2.data in self.adjacency_matrix:
            del self.adjacency_matrix[n1.data][n2.data]
            del self.adjacency_matrix[n2.data][n1.data]

    # Print the adjacency matrix.
    def __str__(self):
        result = ""
        for node, edges in self.nodes.items():
            # Build the string for each node and its edges
            result += f"{node}: " + ", ".join(f"{str(neighbor)} ({weight})" for neighbor, weight in edges.items()) + "\n"
        # Return the graph as a string without trailing newlines
        return result.strip()

    # Import a graph from a file and populate the adjacency matrix.
    def import_from_file(self, file):
        try:
            with open(file, 'r') as f:
                graph_content = f.read()

            if "strict graph" not in graph_content:
                return None

            self.adjacency_matrix = {}
            lines = graph_content.split('\n')

            for line in lines:
                if '--' in line:
                    nodes, attributes = line.split('[')
                    node1, node2 = nodes.strip().split('--')
                    node1 = node1.strip()
                    node2 = node2.strip()
                    weight = 1
                    if 'weight' in attributes:
                        weight = int(attributes.split('=')[1].strip('];'))
                    self.add_node(node1)
                    self.add_node(node2)
                    self.add_edge(GraphNode(node1), GraphNode(node2), weight)

        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as e:
            print("Error occurred while parsing the file:", e)
            return None

    # Perform Depth First Search (DFS) traversal on the graph.
    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        traversal_order = [start]
        for neighbor, weight in self.adjacency_matrix[start].items():
            if neighbor not in visited:
                traversal_order.extend(self.dfs(neighbor, visited))
        return traversal_order
    
# 2. Extend both Graph and Graph2 to implement DFS traversal. Call the method dfs() in both classes. The method should return a list of node in DFS order. [0.3 pts]

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_node(self, data):
        if data not in self.adjacency_list:
            self.adjacency_list[data] = []
            return GraphNode(data)
        return None

    def remove_node(self, node):
        if node.data in self.adjacency_list:
            del self.adjacency_list[node.data]

    def add_edge(self, n1, n2, weight=1):
        if n1.data in self.adjacency_list and n2.data in self.adjacency_list:
            self.adjacency_list[n1.data].append((n2.data, weight))
            self.adjacency_list[n2.data].append((n1.data, weight))

    def remove_edge(self, n1, n2):
        if n1.data in self.adjacency_list and n2.data in self.adjacency_list:
            self.adjacency_list[n1.data] = [(neighbor, weight) for neighbor, weight in self.adjacency_list[n1.data] if neighbor != n2.data]
            self.adjacency_list[n2.data] = [(neighbor, weight) for neighbor, weight in self.adjacency_list[n2.data] if neighbor != n1.data]

    def __str__(self):
        result = ""
        for node, edges in self.nodes.items():
            # Build the string for each node and its edges
            result += f"{node}: " + ", ".join(f"{str(neighbor)} ({weight})" for neighbor, weight in edges.items()) + "\n"
        # Return the graph as a string without trailing newlines
        return result.strip()

    def import_from_file(self, file):
        try:
            with open(file, 'r') as f:
                graph_content = f.read()

            if "strict graph" not in graph_content:
                return None

            self.adjacency_list = {}
            lines = graph_content.split('\n')

            for line in lines:
                if '--' in line:
                    nodes, attributes = line.split('[')
                    node1, node2 = nodes.strip().split('--')
                    node1 = node1.strip()
                    node2 = node2.strip()
                    weight = 1
                    if 'weight' in attributes:
                        weight = int(attributes.split('=')[1].strip('];'))
                    self.add_node(node1)
                    self.add_node(node2)
                    self.add_edge(GraphNode(node1), GraphNode(node2), weight)

        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as e:
            print("Error occurred while parsing the file:", e)
            return None

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        traversal_order = [start]
        for neighbor, i in self.adjacency_list[start]:
            if neighbor not in visited:
                traversal_order.extend(self.dfs(neighbor, visited))
        return traversal_order


# 3. Measure the performance of dfs() on the example graph from D2L (random.dot) [0.3 pts]
    # Repeat the execution of dfs() ten times for each implementation, and report maximum, minimum and average time
    # Discuss the results: which implementation is faster? Why?

def measure_dfs(graph):
    if isinstance(graph, Graph):
        time_taken = timeit.timeit(lambda: graph.dfs(list(graph.adjacency_list.keys())[0]), number=10)
    elif isinstance(graph, Graph2):
        time_taken = timeit.timeit(lambda: graph.dfs(list(graph.adjacency_matrix.keys())[0]), number=10)
    else:
        print("Invalid graph type.")
        return None
    return time_taken


graph_file = "random.dot"

graph1 = Graph()
graph2 = Graph2()

# Import graph from file for both graph1 and graph2
graph1.import_from_file(graph_file)
graph2.import_from_file(graph_file)

execution_times_graph = [measure_dfs(graph1) for i in range(10)]
execution_times_graph2 = [measure_dfs(graph2) for i in range(10)]

max_time_graph = max(execution_times_graph)
min_time_graph = min(execution_times_graph)
avg_time_graph = sum(execution_times_graph) / len(execution_times_graph)

max_time_graph2 = max(execution_times_graph2)
min_time_graph2 = min(execution_times_graph2)
avg_time_graph2 = sum(execution_times_graph2) / len(execution_times_graph2)

print("Graph Performance:")
print(f'Max time: {max_time_graph} seconds')
print(f'Min time: {min_time_graph} seconds')
print(f'Average time: {avg_time_graph} seconds')
print()

print("Graph2 Performance:")
print(f'Max time: {max_time_graph2} seconds')
print(f'Min time: {min_time_graph2} seconds')
print(f'Average time: {avg_time_graph2} seconds')


"""
The faster implementation is not always the same.

Considering these results, we can see that there is no significant difference in performance between the two implementations. 
The choice between using an adjacency list (Graph) and an adjacency matrix (Graph2) depends on various factors such as 
the specific use case, the nature of the graph, and the operations that need to be performed frequently.
In general, adjacency lists tend to be more memory-efficient for sparse graphs (graphs with fewer edges),
while adjacency matrices are more efficient for dense graphs (graphs with many edges). 
"""