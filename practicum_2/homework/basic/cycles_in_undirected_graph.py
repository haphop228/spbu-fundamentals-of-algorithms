import networkx as nx
from typing import Any

from src.plotting import plot_graph

flag = False

def neighbours(G: nx.Graph, node: Any):
    arr = []
    for i in G.edges:
        if (node in i):
            if (i[0] != node):
                arr.append(i[0])
            else:
                arr.append(i[1])
    return arr

TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_w_cycles.edgelist",
]
  
 
 
 
 
    
def has_cycles(G: nx.Graph, node: Any, visited: dict[Any], ancestor=-1) -> None:
    global flag
    if (visited[node] == False and flag == False):
        visited[node] = True
        arr = neighbours(G, node)
        for i in arr:
            if(i != ancestor): # if we want to go to the previous node
                if(visited[i] == True): # if we made a circle and meet TRUE node
                   # print(f"CYCLE! from {node} to {i}")
                    flag = True
                else:
                    has_cycles(G, i, visited, node)
    else:
        return
    







if __name__ == "__main__":
    a = "practicum_2/homework/basic/graph_1_wo_cycles.edgelist"
    b = "practicum_2/homework/basic/graph_2_w_cycles.edgelist"
    tmp = False
    for filename in TEST_GRAPH_FILES:
        if (not tmp):
            i = a
            tmp = True
        else:
            i = b
        G = nx.read_edgelist(i, create_using=nx.Graph)
        #plot_graph(G)
        visited = {n: False for n in G}
        print(f"Graph {filename}: " , end = '')
        has_cycles(G, node="0", visited=visited)
        if (flag == True):
            print("there is a cycle!")
        else:
            print("no cycle here!")
