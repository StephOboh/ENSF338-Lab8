''' 1: Topological sorting can be implemented using an algorithm seen in
class. Which algorithm? Why? [0.2] '''

'''
(I) topological sorting is implemented with a variation of the depth first traversal algorithm. the depth first alogrithm 
goes as far into the nodes as it can before encountering a terminal point then it will make its way back. It will recursively ()
go through the graph/ data. It does this becuase depth first search detects cycles which is important beacuse topological sorting 
garuntees acyclic graphs. 
'''

class Graph:
    def __init__(self):
        # Initialize an empty adjacency list to store the graph
        self.adjacent = {}

    def addNode(self, data):
        # Add a node
        if data not in self.adjacent:
            # Iniitialize
            self.adjacent[data] = []
            # Retur GraphNode object 
            return GraphNode(data)
        # Ifexists return None
        return None

    def removeNode(self, node):
        # Remove a node from the graph if there already 
        if node.data in self.adjacent:
            # Delete from the adjacency list
            del self.adjacent[node.data]

    def addEdge(self, n1, n2, weight=1):
        # Add an edge between two nodes in the graph
        if n1.data in self.adjacent and n2.data in self.adjacent:
            # Add connection between n1 and n2 with given weight
            self.adjacent[n1.data].append((n2.data, weight))
            # Add connection between n2 and n1 with the same weight (assuming undirected graph)
            self.adjacent[n2.data].append((n1.data, weight))

    def removeEdge(self, n1, n2):
        # Remove an edge between two nodes in the graph
        if n1.data in self.adjacent and n2.data in self.adjacent:
            # Remove the connection between n1 and n2
            self.adjacent[n1.data] = [(neighbor, weight) for neighbor, weight in self.adjacent[n1.data] if neighbor != n2.data]
            # Remove the connection between n2 and n1
            self.adjacent[n2.data] = [(neighbor, weight) for neighbor, weight in self.adjacent[n2.data] if neighbor != n1.data]

    def printGraph(self):
        # Print the graph
        for node in self.adjacent:
            connections = self.adjacent[node]
            print(f"Node {node} connects to:")
            for neighbor, weight in connections:
                print(f"  {neighbor} with weight {weight}\n")

    def importFromFile(self, file):
        try:
            with open(file, 'r') as f:
                graph_content = f.read()    #read the file 

            # veriffy if the content indicates a graph (assuming DOT format)
            if "strict graph" not in graph_content:
                return None

            # restart the adjacency list
            self.adjacent = {}
            lines = graph_content.split('\n')

            for line_str in lines:
                if '--' in line_str:
                    # retrieve nodes and connections
                    nodes_str, attributes_str = line_str.split('[')
                    node1_str, node2_str = nodes_str.strip().split('--')
                    node1_str, node2_str = node1_str.strip(), node2_str.strip()
                
                    weight_val = 1
                    if 'weight' in attributes_str:
                        # retrieve weight if asked
                        weight_val = int(attributes_str.split('=')[1].strip('];'))
                    
                    #add nodes and edge to the graph
                    self.addNode(node1_str)
                    self.addNode(node2_str)
                    self.addEdge(GraphNode(node1_str), GraphNode(node2_str), weight_val)


        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as e: #other errors 
            print("Error occurred while parsing the file:", e)
            return None


    def toposort(self): #we perfrom topological sort 
        if not self.isdag():
            return None
        
        visited = set() 
        result = []     
        
        def dfs_topo(node): #depth first search 
            visited.add(node)
            for neighbor, _ in self.adjacent.get(node, []):
                if neighbor not in visited:
                    dfs_topo(neighbor)
            result.append(node)
        
        for node in self.adjacent:
            if node not in visited:
                dfs_topo(node)
        
        return result[::-1]  # reverse to get topological ordering
        #method that checks if the graph is a Directed Acyclic Graph (DAG)
    
    
    # using depth first search
    def isdag(self):
        visited_nodes = set() # set to store visited nodes
        current_path = set()   #set to store nodes in current path

        def dfs(node):
            #returns bool true if a cycle is detected otherwise bool false 
            visited_nodes.add(node)
            current_path.add(node)
            for neighbor, _ in self.adjacent.get(node, []):
                if neighbor not in visited_nodes:
                    if dfs(neighbor):
                        return True
                elif neighbor in current_path:
                    return True
            current_path.remove(node)
            return False
        
        for node in self.adjacent:
            if node not in visited_nodes:
                if dfs(node):
                    return False
        return True


#forgot to initialize; truly a faceplam moment 

class GraphNode:
    #initalize
    def __init__(self, data):
        self.data = data

#was testing to see if it worked 

# graph = Graph()

# node1 = graph.addNode('A')
# node2 = graph.addNode('B')
# node3 = graph.addNode('C')
# node4 = graph.addNode('D')

# graph.addEdge(node1, node2)
# graph.addEdge(node2, node3)
# graph.addEdge(node3, node4)

# print("Graph:")
# graph.printGraph()

# print("DAG??", graph.isdag())

# print("Topological sorting:")
# topological_order = graph.toposort()
# if topological_order:
#     print(topological_order)
# else:
#     print("cant sort.")
