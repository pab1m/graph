from collections import defaultdict
import timeit
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, vertices):

        """
        Конструктор класу Graph.

        Параметри:
        - вершини (int): Кількість вершин у графі.

        Атрибути:
        - V (int): Кількість вершин у графі.
        - graph (defaultdict): Словник для зберігання списків суміжності графа.
        - time (int): Змінна для відстеження часу під час обходу DFS.
        """

        self.V = vertices
        self.graph = defaultdict(list)
        self.time = 0

    def add_edge(self, u, v):

        """
        Додає ненапрямлене ребро між вершинами u та v.

        Параметри:
        - u (int): Індекс першої вершини.
        - v (int): Індекс другої вершини.
        """

        self.graph[u].append(v)
        self.graph[v].append(u)

    def articulation_points_dfs(self, u, visited, disc, low, parent, ap):

        """
        DFS-обхід для знаходження точок з'єднання.

        Параметри:
        - u (int): Поточна вершина для обходу.
        - відвідані (list): Список для відстеження відвіданих вершин.
        - disc (list): Список для відстеження часу відкриття вершин.
        - low (list): Список для відстеження найменшого часу відкриття вершин, до яких можливий back edge.
        - parent (list): Список для відстеження батьківської вершини під час обходу.
        - ap (list): Список для відстеження точок з'єднання.

        Вивід:
        - Змінює список ap, позначаючи вершини як точки з'єднання.
        """

        children = 0
        disc[u] = self.time
        low[u] = self.time
        self.time += 1
        visited[u] = True

        for v in self.graph[u]:
            if not visited[v]:
                children += 1
                parent[v] = u
                self.articulation_points_dfs(v, visited, disc, low, parent, ap)

                low[u] = min(low[u], low[v])

                if low[v] >= disc[u] and parent[u] != -1:
                    ap[u] = True

                if parent[u] == -1 and children > 1:
                    ap[u] = True
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    def find_articulation_points_dfs(self):

        """
       Запускає DFS-обхід для знаходження точок з'єднання, визначення їх кількості та індексів.

       Повертає:
       - Кількість точок з'єднання, індекси точок та час виконання алгоритму.
       """

        visited = [False] * self.V
        disc = [-1] * self.V
        low = [-1] * self.V
        parent = [-1] * self.V
        ap = [False] * self.V
        self.time = 0

        start_time = timeit.default_timer()

        for i in range(self.V):
            if not visited[i]:
                self.articulation_points_dfs(i, visited, disc, low, parent, ap)

        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time

        articulation_points = [i for i in range(self.V) if ap[i]]
        return len(articulation_points), articulation_points, elapsed_time

    def articulation_points_tarjan(self, u, low, disc, parent, ap):

        """
       Алгоритм Тар'яна для знаходження точок з'єднання.

       Параметри:
       - u (int): Поточна вершина для обходу.
       - low (list): Список для відстеження найменшого часу відкриття вершин, до яких можливий back edge.
       - disc (list): Список для відстеження часу відкриття вершин.
       - parent (list): Список для відстеження батьківської вершини під час обходу.
       - ap (list): Список для відстеження точок з'єднання.

       Вивід:
       - Змінює список ap, позначаючи вершини як точки з'єднання.
       """

        children = 0
        disc[u] = self.time
        low[u] = self.time
        self.time += 1

        for v in self.graph[u]:
            if disc[v] == -1:
                children += 1
                parent[v] = u
                self.articulation_points_tarjan(v, low, disc, parent, ap)

                low[u] = min(low[u], low[v])

                if low[v] >= disc[u] and parent[u] != -1:
                    ap[u] = True

                if parent[u] == -1 and children > 1:
                    ap[u] = True
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    def find_articulation_points_tarjan(self):

        """
        Запускає алгоритм Тар'яна для знаходження точок з'єднання та визначення їх кількості та індексів.

        Повертає:
        - Кількість точок з'єднання, індекси точок та час виконання алгоритму.
        """

        disc = [-1] * self.V
        low = [-1] * self.V
        parent = [-1] * self.V
        ap = [False] * self.V
        self.time = 0

        start_time = timeit.default_timer()

        for i in range(self.V):
            if disc[i] == -1:
                self.articulation_points_tarjan(i, low, disc, parent, ap)

        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time

        articulation_points = [i for i in range(self.V) if ap[i]]
        return len(articulation_points), articulation_points, elapsed_time


def get_user_input():
    num_vertices = int(input("Введіть кількість вершин: "))
    edges = []

    print("Введіть ребра (вершина1, вершина2) через пробіл:")
    for _ in range(num_vertices):
        edge = tuple(map(int, input().split()))
        edges.append(edge)

    return num_vertices, edges


def drawing_graph(graph_edges):
    graph = nx.Graph()
    graph.add_edges_from(graph_edges)

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_weight='bold',
            node_color='lightblue', font_color='red', node_size=700)
    plt.show()


def main():
    num_vertices, user_edges = get_user_input()

    graph = Graph(num_vertices)
    for edge in user_edges:
        graph.add_edge(*edge)

    num_points_dfs, points_dfs, elapsed_time_dfs = graph.find_articulation_points_dfs()
    print(f"DFS: Кількість точок з'єднання: {num_points_dfs}")
    print(f"DFS: Індекси точок з'єднання: {points_dfs}")
    print(f"DFS: Час виконання алгоритму: {elapsed_time_dfs:.9f} секунд")

    print("-" * 50)
    num_points_tarjan, points_tarjan, elapsed_time_tarjan = graph.find_articulation_points_tarjan()
    print(f"Tarjan: Кількість точок з'єднання: {num_points_tarjan}")
    print(f"Tarjan: Індекси точок з'єднання: {points_tarjan}")
    print(f"Tarjan: Час виконання алгоритму: {elapsed_time_tarjan:.9f} секунд")

    drawing_graph(user_edges)


if __name__ == "__main__":
    main()
