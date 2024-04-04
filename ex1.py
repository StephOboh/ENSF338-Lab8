# Import the regex module for pattern matching
import re

class GraphNode:
    # Initialize a GraphNode with data
    def __init__(self, data):
        self.data = data

    # Representation of a GraphNode object
    def __repr__(self):
        return f"GraphNode({self.data})"

class Graph:
    # Initialize an empty dictionary to hold nodes and their edges
    def __init__(self):
        self.nodes = {}

    # Ensure uniqueness of nodes based on their data
    def add_node(self, data):
        for node in self.nodes:
            # Return existing node if data matches
            if node.data == data:
                return node
        # Create a new GraphNode
        new_node = GraphNode(data)
        # Add new node with an empty edge dictionary
        self.nodes[new_node] = {}
        # Return the new node
        return new_node

    # Remove a node and its connected edges from the graph
    def remove_node(self, node):
        if node in self.nodes:
            for neighbor in list(self.nodes[node]):
                # Remove all edges connected to the node
                self.remove_edge(node, neighbor)
            # Delete the node from the graph
            del self.nodes[node]

    # Add an edge between two nodes with a given weight
    def add_edge(self, n1, n2, weight=1):
        if n1 in self.nodes and n2 in self.nodes:
            # Add edge from n1 to n2 with weight
            self.nodes[n1][n2] = weight
            # Add edge from n2 to n1 with weight (undirected graph)
            self.nodes[n2][n1] = weight

    # Remove an edge between two nodes
    def remove_edge(self, n1, n2):
        if n1 in self.nodes and n2 in self.nodes:
            if n2 in self.nodes[n1]:
                # Remove edge from n1 to n2
                del self.nodes[n1][n2]
            if n1 in self.nodes[n2]:
                # Remove edge from n2 to n1
                del self.nodes[n2][n1]

    # Import graph structure from a file
    def import_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                # Read file content and strip whitespace
                content = file.read().strip()

            # Check for correct graph declaration
            header_pattern = re.compile(r"^strict graph \w+ \{$")
            if not header_pattern.search(content):
                # Return None if graph declaration is incorrect
                return None
            
            # Extract edge information
            edge_pattern = re.compile(r"(\w+)\s*--\s*(\w+)(?:\s*\[weight=(\d+)\])?\s*;", re.MULTILINE)
            edges = edge_pattern.findall(content)  # Find all edges in the content

            # Reset the graph
            self.nodes.clear()

            # Process each edge
            for n1_data, n2_data, weight in edges:
                # Add or get node1
                node1 = self.add_node(n1_data)
                # Add or get node2
                node2 = self.add_node(n2_data)
                # Use provided weight or default to 1
                weight = int(weight) if weight else 1
                # Add edge between node1 and node2
                self.add_edge(node1, node2, weight)
                
        except Exception as e:
            # Return None in case of errors
            return None

        # Return the graph object after successful import
        return self

    # Create a string representation of the graph
    def __str__(self):
        result = ""
        for node, edges in self.nodes.items():
            # Build the string for each node and its edges
            result += f"{node}: " + ", ".join(f"{str(neighbor)} ({weight})" for neighbor, weight in edges.items()) + "\n"
        # Return the graph as a string without trailing newlines
        return result.strip()
