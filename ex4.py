import timeit
import random
import re

class GraphNode:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"GraphNode({self.data})"


# 1. Starting from the Graph class created in Exercise 1, create a Graph2 class which uses (you guessed it) an adjacency matrix to keep track of the edges [0.9 pts]
    # Each location in the matrix must be 0 if an edge is not present, and W (where W is the edge’s weight) if an edge is present

class Graph2:
    def __init__(self):
        self.adjacency_matrix = {}

    def add_node(self, data):
        if data not in self.adjacency_matrix:
            self.adjacency_matrix[data] = {}
            return GraphNode(data)
        return None

    def remove_node(self, node):
        if node.data in self.adjacency_matrix:
            del self.adjacency_matrix[node.data]
            for key in self.adjacency_matrix:
                if node.data in self.adjacency_matrix[key]:
                    del self.adjacency_matrix[key][node.data]

    def add_edge(self, n1, n2, weight=1):
        if n1.data in self.adjacency_matrix and n2.data in self.adjacency_matrix:
            self.adjacency_matrix[n1.data][n2.data] = weight
            self.adjacency_matrix[n2.data][n1.data] = weight

    def remove_edge(self, n1, n2):
        if n1.data in self.adjacency_matrix and n2.data in self.adjacency_matrix:
            del self.adjacency_matrix[n1.data][n2.data]
            del self.adjacency_matrix[n2.data][n1.data]

    def print_graph(self):
        for node in self.adjacency_matrix:
            connections = self.adjacency_matrix[node]
            print(f"Node {node} connects to:")
            for neighbor, weight in connections.items():
                print(f"  {neighbor} with weight {weight}\n")

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

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        traversal_order = [start]
        for neighbor in self.adjacency_matrix[start]:
            if neighbor not in visited:
                traversal_order.extend(self.dfs(neighbor, visited))
        return traversal_order

# 2. Extend both Graph and Graph2 to implement DFS traversal. Call the method dfs() in both classes. The method should return a list of node in DFS order. [0.3 pts]

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, data):
        for node in self.nodes:
            if node.data == data:
                return node
        new_node = GraphNode(data)
        self.nodes[new_node] = {}
        return new_node

    def remove_node(self, node):
        if node in self.nodes:
            for neighbor in list(self.nodes[node]):
                self.remove_edge(node, neighbor)
            del self.nodes[node]

    def add_edge(self, n1, n2, weight=1):
        if n1 in self.nodes and n2 in self.nodes:
            self.nodes[n1][n2] = weight
            self.nodes[n2][n1] = weight

    def remove_edge(self, n1, n2):
        if n1 in self.nodes and n2 in self.nodes:
            if n2 in self.nodes[n1]:
                del self.nodes[n1][n2]
            if n1 in self.nodes[n2]:
                del self.nodes[n2][n1]

    def import_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read().strip()

            header_pattern = re.compile(r"^strict graph \w+ \{$")
            if not header_pattern.search(content):
                return None
            
            edge_pattern = re.compile(r"(\w+)\s*--\s*(\w+)(?:\s*\[weight=(\d+)\])?\s*;", re.MULTILINE)
            edges = edge_pattern.findall(content)

            self.nodes.clear()

            for n1_data, n2_data, weight in edges:
                node1 = self.add_node(n1_data)
                node2 = self.add_node(n2_data)
                weight = int(weight) if weight else 1
                self.add_edge(node1, node2, weight)
                
        except Exception as e:
            return None

        return self

    def __str__(self):
        result = ""
        for node, edges in self.nodes.items():
            result += f"{node}: " + ", ".join(f"{str(neighbor)} ({weight})" for neighbor, weight in edges.items()) + "\n"
        return result.strip()

    def dfs(self, start):
        visited = set()
        traversal_order = []
        self._dfs_recursive(start, visited, traversal_order)
        return traversal_order

    def _dfs_recursive(self, node, visited, traversal_order):
        visited.add(node)
        traversal_order.append(node)
        for neighbor in self.nodes[node]:
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited, traversal_order)


# 3. Measure the performance of dfs() on the example graph from D2L (random.dot) [0.3 pts]
    # Repeat the execution of dfs() ten times for each implementation, and report maximum, minimum and average time
    # Discuss the results: which implementation is faster? Why?

def measure_dfs(graph, start_node):
    time_taken = timeit.timeit(lambda: graph.dfs(start_node), number=10)
    return time_taken

graph_file = "random.dot"

graph1 = Graph()
graph2 = Graph2()

graph1.import_from_file(graph_file)
graph2.import_from_file(graph_file)


# Import graphs from file
# if graph1.import_from_file(graph_file) is None:
#     print("Failed to import graph from file for Graph1. Exiting.")
#     exit()

# if graph2.import_from_file(graph_file) is None:
#     print("Failed to import graph from file for Graph2. Exiting.")
#     exit()

# Measure DFS performance for Graph
if len(graph1.nodes) > 0:
    execution_times_graph1 = [measure_dfs(graph1, list(graph1.nodes.keys())[0]) for _ in range(10)]
    max_time_graph1 = max(execution_times_graph1)
    min_time_graph1 = min(execution_times_graph1)
    avg_time_graph1 = sum(execution_times_graph1) / len(execution_times_graph1)

    # Print performance results for Graph
    print("Performance of dfs() for Graph:")
    print(f'Max time: {max_time_graph1} seconds')
    print(f'Min time: {min_time_graph1} seconds')
    print(f'Average time: {avg_time_graph1} seconds')
else:
    print("Graph1 is empty. Cannot measure DFS performance.")

# Measure DFS performance for Graph2
if len(graph2.adjacency_matrix) > 0:
    execution_times_graph2 = [measure_dfs(graph2, list(graph2.adjacency_matrix.keys())[0]) for _ in range(10)]
    max_time_graph2 = max(execution_times_graph2)
    min_time_graph2 = min(execution_times_graph2)
    avg_time_graph2 = sum(execution_times_graph2) / len(execution_times_graph2)

    # Print performance results for Graph2
    print("\nPerformance of dfs() for Graph2:")
    print(f'Max time: {max_time_graph2} seconds')
    print(f'Min time: {min_time_graph2} seconds')
    print(f'Average time: {avg_time_graph2} seconds')
else:
    print("Graph2 is empty. Cannot measure DFS performance.")