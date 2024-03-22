class Graph:
    def __init__(self):
        self

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def isdag(self):
        visited = set()
        stack = set()

        def dfs(node):
            visited.add(node)
            stack.add(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in stack:
                    return True
            stack.remove(node)
            return False

        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    return False
        return True


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def isdag(self):
        visited = set()
        stack = set()

        def dfs(node):
            visited.add(node)
            stack.add(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in stack:
                    return True
            stack.remove(node)
            return False

        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    return False
        return True

    def toposort(self):
        if not self.isdag():
            return None

        visited = set()
        topo_order = []

        def dfs(node):
            visited.add(node)
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    dfs(neighbor)
            topo_order.append(node)

        for node in self.graph:
            if node not in visited:
                dfs(node)

        return topo_order[::-1]

