class Graph:
    def __init__(self, graph_dict=None):
        if graph_dict is None:
            graph_dict = {}
        self._graph_dict = graph_dict

    def add_edge(self, edge):
        edge = set(edge)
        vertex1, vertex2 = tuple(edge)
        for x, y in [(vertex1, vertex2), (vertex2, vertex1)]:
            if x in self._graph_dict:
                self._graph_dict[x].append(y)
            else:
                self._graph_dict[x] = [y]

    def find_path(self, start_vertex, end_vertex, path=None):
        if path is None:
            path = []
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        shortest = None
        for node in self._graph_dict[start_vertex]:
            if node not in path:
                new_path = self.find_path(node, end_vertex, path)
                if new_path and (not shortest or len(new_path) < len(shortest)):
                    shortest = new_path
        return shortest
