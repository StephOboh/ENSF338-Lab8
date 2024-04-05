"""
TO DO:
- Make the mst() method return a Graph object describing the spanning tree ?????

"""

''' 2. Implement the UNION-FIND cycle detection algorithm for undirected graphs. [0.6 pts] '''
class UnionFind:
    def __init__(self, n):
        # Initialize the UnionFind data structure with 'n' elements
        # Initially, each element is its own parent and has a rank of 0
        self.parent = [i for i in range(n)]  # 'parent' list to store the parent of each element
        self.rank = [0] * n  # 'rank' list to store the rank (depth) of each element

    def find(self, u):
        # Find operation to determine the root (representative) of the set containing element 'u'
        if self.parent[u] != u:
            # If 'u' is not its own parent, recursively find the root of its parent
            self.parent[u] = self.find(self.parent[u])  # Path compression: update the parent to the root
        return self.parent[u]  # Return the root of the set containing element 'u'

    def union(self, u, v):
        # Union operation to merge the sets containing elements 'u' and 'v'
        root_u = self.find(u)  # Find the root of the set containing 'u'
        root_v = self.find(v)  # Find the root of the set containing 'v'

        if root_u == root_v:
            # If 'u' and 'v' have the same root, they are already in the same set
            return False  # No need to merge, return False indicating no change in the sets

        # Perform union by rank to merge the smaller tree into the larger tree
        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v  # Attach 'root_u' to 'root_v'
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u  # Attach 'root_v' to 'root_u'
        else:
            # If both roots have the same rank, arbitrarily choose one to be the parent
            self.parent[root_v] = root_u  # Attach 'root_v' to 'root_u'
            self.rank[root_u] += 1  # Increase the rank of 'root_u' by 1

        return True  # Union successful, return True indicating a change in the sets


''' 3. Use your implementation of UNION-FIND to implement the full Kruskal algorithm as discussed in class. 
       Implement Kruskal as a method called mst() as part of your Graph class. The method should return a Graph object describing the spanning tree. [0.6 pts] '''

class Graph:
    def __init__(self, vertices):
        # Initialize the Graph object with a given number of vertices
        self.V = vertices  # Number of vertices in the graph
        self.graph = []     # List to store the edges of the graph

    def add_edge(self, u, v, w):
        # Add an edge to the graph with vertices 'u' and 'v', and weight 'w'
        self.graph.append([u, v, w])  # Append the edge (u, v, w) to the graph list

    def mst(self):
        # Compute MST using Kruskal's algorithm
        # Sort the edges of the graph based on their weights
        self.graph.sort(key=lambda x: x[2])

        # Initialize an empty graph to represent the MST
        mst_tree = Graph(self.V)

        # Initialize a UnionFind data structure to detect cycles and manage sets
        uf = UnionFind(self.V)

        # Initialize variables to keep track of the number of edges added to the MST
        edges_added = 0  # Number of edges added to the MST
        index = 0        # Index to iterate over the sorted edges

        # Iterate over the sorted edges until the MST is complete
        while edges_added < self.V - 1:
            # Get the next edge (u, v, w) from the sorted list of edges
            u, v, w = self.graph[index]
            index += 1  # Move to the next edge in the sorted list

            # Find the root (representative) of the sets containing vertices 'u' and 'v'
            u_root = uf.find(u)
            v_root = uf.find(v)

            # Check if adding the edge (u, v) creates a cycle in the MST
            if u_root != v_root:
                # If adding the edge does not create a cycle, add it to the MST
                mst_tree.add_edge(u, v, w)
                # Perform union operation to merge the sets containing vertices 'u' and 'v'
                uf.union(u_root, v_root)
                edges_added += 1  # Increment the number of edges added to the MST

        return mst_tree  # Return the MST as a Graph object
    
    # Print the MST
    def print_mst(self):
        print("Mininmum Spanning Tree [Node, Node, EdgeWeight]:")
        for edge in self.graph:
            print(edge)

# TESTING
# Create the graph - THAT IS IN EX3.PDF
g = Graph(5)

g.add_edge(0, 1, 2)
g.add_edge(0, 2, 6)
g.add_edge(1, 2, 4)
g.add_edge(1, 3, 14)
g.add_edge(2, 3, 20)
g.add_edge(2, 4, 10)
g.add_edge(3, 4, 4)

# Compute MST using Kruskal's algorithm
mst = g.mst()

# Print the edges of the MST -- SHOULD BE THE SAME AS MST IN EX3.PDF
mst.print_mst()
