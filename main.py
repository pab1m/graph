class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = [[] for _ in range(vertices)]
        self.time = 0

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def articulation_points(self):
        visited = [False] * self.vertices
        disc = [float("inf")] * self.vertices
        low = [float("inf")] * self.vertices
        parent = [-1] * self.vertices
        ap = [False] * self.vertices

        def dfs(u):
            nonlocal visited, disc, low, parent, ap
            children = 0
            visited[u] = True
            disc[u] = self.time
            low[u] = self.time
            self.time += 1

            for v in self.graph[u]:
                if not visited[v]:
                    children += 1
                    parent[v] = u
                    dfs(v)
                    low[u] = min(low[u], low[v])

                    if low[v] >= disc[u] or (parent[u] == -1 and children > 1):
                        ap[u] = True
                elif v != parent[u]:
                    low[u] = min(low[u], disc[v])

        for i in range(self.vertices):
            if not visited[i]:
                dfs(i)

        result = [i for i in range(self.vertices) if ap[i]]
        return result


# Приклад використання:
g = Graph(5)
g.add_edge(1, 2)
g.add_edge(2, 2)
# g.add_edge(2, 1)
g.add_edge(3, 3)
g.add_edge(4, 4)

articulation_points = g.articulation_points()

print("Кількість точок з'єднання:", len(articulation_points))
print("Їхні індекси:", articulation_points)


import networkx as nx
import matplotlib.pyplot as plt

# Граф
edges = [(1, 2), (2, 2),  (3, 3), (4, 4)]
g = nx.Graph()
g.add_edges_from(edges)

# Візуалізація графу
pos = nx.spring_layout(g)  # Позиціонування вершин
nx.draw(g, pos, with_labels=True, font_weight='bold', node_color='lightblue', font_color='red', node_size=700)
plt.title("Неорієнтований граф")
plt.show()
