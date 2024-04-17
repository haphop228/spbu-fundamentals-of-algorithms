from collections import deque
import networkx as nx

def bfs(graph, s, t, parent):
  visited = [False] * len(graph)
  queue = deque()

  queue.append(s)
  visited[s] = True

  while queue:
    u = queue.popleft()
    
    for i in graph.edges():
        if not visited[int(i[0])]:
            queue.append(int(i[0]))
            visited[int(i[0])] = True
            parent[int(i[0])] = u
  return visited[t]
"""
    for ind, val in enumerate(graph[u]):
      print(ind, " ", val)
      if not visited[ind] and val > 0:
        queue.append(ind)
        visited[ind] = True
        parent[ind] = u
"""

def edmonds_carp(graph, source, sink):
  parent = [-1] * len(graph)
  max_flow = 0

  while bfs(graph, source, sink, parent):
    path_flow = float("Inf")
    s = sink
    while s != source:
      path_flow = min(path_flow, graph[parent[s]][s])
      s = parent[s]

    max_flow += path_flow

    v = sink
    while v != source:
      u = parent[v]
      graph[u][v] -= path_flow
      graph[v][u] += path_flow
      v = u

  return max_flow

# Example usage
graph = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.Graph)
"""
graph = [[0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]]
        """
source = 0
sink = 5
parent = [-1] * len(graph)
b = graph.edges()
print(b)
a = bfs(graph, 0, 5, parent)
print(a)
max_flow = edmonds_carp(graph, source, sink)

print("Maximum flow:", max_flow)
