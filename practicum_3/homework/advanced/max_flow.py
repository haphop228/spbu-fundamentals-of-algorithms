from typing import Any
import collections
from src.plotting import plot_graph
import networkx as nx
import numpy as np

def bfs(G, s, t, parent): 
    visited = []
    queue = set()
    #collections.deque([s])
    
    visited.append(str(s))
    queue.add(s)
    while queue: 
        node = int(queue.pop())
        for neighbour in G.neighbors(str(node)): 
            if neighbour not in visited: 
                visited.append(neighbour)
                print(visited) 
                parent[int(neighbour)] = node
                queue.add(neighbour)
    return visited[t]
                

def max_flow(G: nx.Graph, s: Any, t: Any) -> int:
    value: int = 0
    parent = [-1] * len(G.nodes())
    while bfs(G, s, t, parent):
        pass
    
    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_1.edgelist", create_using=nx.DiGraph)
    #plot_graph(G)
    #G.remove_edge('4', '5')
    #G.remove_edge('3', '5')
    #print(G)
    #print("EDGES:")
    #print(G.edges())
    #dict = nx.coloring.greedy_color(G, strategy="connected_sequential_bfs")   
    #print(dict)
    #parent = [-1] * len(G.nodes())
    #a = bfs(G, 0, 5, parent)
    val = max_flow(G, s=0, t=5)
    #print(f"Maximum flow is {val}. Should be 23")
