# 2. Implement the UNION-FIND cycle detection algorithm for undirected graphs. [0.6 pts]
class UnionFind:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            return False

        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1

        return True


# 3. Use your implementation of UNION-FIND to implement the full Kruskal algorithm as discussed in class. 
# Implement Kruskal as a method called mst() as part of your Graph class. The method should return a Graph object describing the spanning tree. [0.6 pts]

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def mst(self):
        self.graph.sort(key=lambda x: x[2])
        mst_tree = Graph(self.V)
        uf = UnionFind(self.V)
        edges_added = 0
        index = 0

        while edges_added < self.V - 1:
            u, v, w = self.graph[index]
            index += 1
            u_root = uf.find(u)
            v_root = uf.find(v)

            if u_root != v_root:
                mst_tree.add_edge(u, v, w)
                uf.union(u_root, v_root)
                edges_added += 1

        return mst_tree


# This mst() method of the Graph class implements Kruskal's algorithm using the Union-Find data structure to detect cycles and construct the minimum spanning tree of the graph. 
# The method returns a Graph object describing the spanning tree. 