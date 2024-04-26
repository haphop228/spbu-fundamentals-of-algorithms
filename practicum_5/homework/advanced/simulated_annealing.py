from typing import Protocol
import numpy as np
from numpy.typing import NDArray
import networkx as nx

from src.plotting import plot_graph, plot_loss_history

NDArrayInt = NDArray[np.int_]

average_mistakes = []

class GraphColoringSolver(Protocol):
    def __call__(
        G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
    ) -> NDArrayInt:
        pass

def number_of_conflicts(G, colors):
    set_colors(G, colors)
    n = 0
    for n_in, n_out in G.edges:
        if G.nodes[n_in]["color"] == G.nodes[n_out]["color"]:
            n += 1
    return n

def set_colors(G, colors):
    for n, color in zip(G.nodes, colors):
        G.nodes[n]["color"] = color

def tweak(colors, n_max_colors, G):
    new_colors = colors.copy()
    #arr_random_index = []
    for j in range(len(colors) // 20):
        random_index = np.random.randint(low=0, high=len(colors))
        #arr_random_index.append(random_index)
        #new_colors[random_index] = np.random.randint(0, n_max_colors - 1)
    new_colors[random_index] = np.random.randint(0, n_max_colors - 1)
    #new_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))
    return new_colors

def temperature_changing(temperature, i) -> int:
    lamda = 0.99
    #* int((i // 5) + 1)
    #iter = 500 - 2 * i
    temperature = temperature * lamda
    #temperature = temperature ** np.log(temperature) * lamda
    #temperature = temperature * np.cos(temperature) 
    #temperature = temperature ** np.log(temperature) * lamda
    #np.exp(temperature) 
    return temperature

def new_tweaks(colors, n_max_colors):
    new_colors = colors.copy()
    for j in range(len(colors) // 30):
        random_index1 = np.random.randint(low=0, high=len(colors))
        random_index2 = np.random.randint(low=0, high=len(colors))
        #arr_random_index.append(random_index)
        #new_colors[random_index1] = np.random.randint(0, n_max_colors - 1)
        new_colors[random_index1] = new_colors[random_index2]
    
    #new_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))
    return new_colors

def new_new_tweaks(colors, n_max_colors):
    new_colors = colors.copy()
    rand_color = np.random.randint(0, n_max_colors - 1)
    random_index1 = np.random.randint(low=0, high=len(colors))
    if (random_index1 + 1) in new_colors:
        while (new_colors[random_index1] != new_colors[random_index1 + 1] and random_index1 < len(colors) - 1):
            new_colors[random_index1] = rand_color
            random_index1 +=1
        
    return new_colors

def new_new_new_tweaks(G: nx.Graph, colors, n_max_colors):
    new_colors = colors.copy()
    #print(set(new_colors))
    
    # 13 mistakes one color, >= 8
    probabiliy = 0.7
    num = np.random.uniform(0, 1)
    rand_node = np.random.randint(low=0, high=len(G.nodes))
    color_of_node_we_check = colors[rand_node]
    rand_color = np.random.randint(0, n_max_colors)
    
    while (color_of_node_we_check == rand_color):
        rand_color = np.random.randint(0, n_max_colors)
        
    if len(list(G.neighbors(rand_node))) >= 8:
        for i in G.neighbors(rand_node):
            new_colors[i] = rand_color
    else:
        new_colors[rand_node] = rand_color
            
    return new_colors

def new_new_new_new_tweaks(G: nx.Graph, colors, n_max_colors):
    new_colors = colors.copy()
    # 13 mistakes one color, >= 8
    probabiliy = 0.7
    num = np.random.uniform(0, 1)
    rand_node = np.random.randint(low=0, high=len(G.nodes))
    color_of_node_we_check = colors[rand_node]
    rand_color = np.random.randint(0, n_max_colors - 1)
    
    arr_of_neighbors_colors = np.zeros(n_max_colors - 1, dtype=np.int_)
    for i in G.neighbors(rand_node):
        arr_of_neighbors_colors[new_colors[i]]+=1
    
    color = min(arr_of_neighbors_colors)
    for i in range(len(arr_of_neighbors_colors)):
        if arr_of_neighbors_colors[i] == color:
            index = i
    for i in G.neighbors(rand_node):
        new_colors[i] = arr_of_neighbors_colors[index]
            
    return new_colors

def tweak(colors, n_max_colors):
    new_colors = colors.copy()
    random_index = np.random.randint(0, len(colors))
    new_color = np.random.randint(0, n_max_colors - 1)
    new_colors[random_index] = new_color
    return new_colors

def tweaks(colors, n_max_colors):
    new_colors = colors.copy()
    random_index = np.random.randint(0, len(colors))
    new_colors[random_index] = np.random.randint(0, n_max_colors - 1)
    
    return new_colors

def solve_via_simulated_annealing_restarts(
    solver: GraphColoringSolver, 
    G: nx.Graph,
    n_max_colors: int, 
    initial_colors: NDArrayInt,
    n_iters: int,
    n_restarts: int
)-> NDArrayInt:
    loss_history = np.zeros((n_restarts, n_iters), dtype=np.int_)
    for i in range(n_restarts):
        print(f"Restart #{i + 1}")
        initial_colors = np.random.randint(0, n_max_colors - 1, len(G.nodes))
        set_colors(G, initial_colors)  
        loss_history_per_run = solver(G, n_max_colors, initial_colors, n_max_iters)
        loss_history[i, :] = loss_history_per_run
    return loss_history
    

def solve_via_simulated_annealing(
    G: nx.Graph,
    n_max_colors: int, 
    initial_colors: NDArrayInt,
    n_iters: int,
):
    global average_mistakes
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    cur_colors = initial_colors.copy()
    next_colors = initial_colors.copy()
    
    counter = 0
    temperature = 1
    arr_of_loss_history = []
    
    probability_history = np.zeros((n_iters,), dtype=np.float64)
    temperature_history = np.zeros((n_iters,), dtype=np.float64)
    
    for i in range(n_iters):
        if(temperature >= 0):
            loss_history[i] = number_of_conflicts(G, cur_colors)
            arr_of_loss_history.append(loss_history[i])
            next_colors = new_new_new_tweaks(G, cur_colors, n_max_colors)
            #next_colors = new_new_new_new_tweaks(G, cur_colors, n_max_colors)
            #next_colors = tweak(cur_colors, n_max_colors)

            cur_confl = number_of_conflicts(G, cur_colors)
            new_confl = number_of_conflicts(G, next_colors)
            
            delta_energy = cur_confl - new_confl
            probability = np.exp((abs(delta_energy) * (-1)) / temperature)
            
            probability_history[counter] = probability

            num = np.random.uniform(0, 1)
            if (delta_energy <= 0 and num <= probability):
                cur_colors = next_colors
            elif delta_energy > 0:
                cur_colors = next_colors
            temperature = temperature_changing(temperature=temperature, i=i)
            temperature_history[counter] = temperature
            counter+=1
        
    #print(min(arr_of_loss_history))
    average_mistakes.append(min(arr_of_loss_history))
    #plot_loss_history(probability_history)
    #plot_loss_history(temperature_history) 
    return loss_history

if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    #plot_graph(G)
    
    n_max_iters = 500
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    """
    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    """
    n_restarts = 10
    loss_history = solve_via_simulated_annealing_restarts(
        solve_via_simulated_annealing,
        G,
        n_max_colors,
        initial_colors,
        n_max_iters,
        n_restarts,
    )
    #plot_loss_history(loss_history)
    print(sum(average_mistakes) / n_restarts)
    print(average_mistakes[0])
    #plot_loss_history(loss_history)
