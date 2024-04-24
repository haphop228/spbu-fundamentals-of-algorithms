import numpy as np
from numpy.typing import NDArray
import networkx as nx

from src.plotting import plot_graph, plot_loss_history

NDArrayInt = NDArray[np.int_]

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
    random_index = np.random.randint(0, len(colors))
    new_colors[random_index] = np.random.randint(0, n_max_colors - 1)
    new_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))
    return new_colors

def temperature_changing(temperature, i) -> int:
    temperature = temperature - (((i + 1)))
    return temperature

def new_tweaks(colors, n_max_colors):
    new_colors = colors.copy()
    rand_num1 = np.random.randint(low=0, high=len(colors))
    rand_num2 = np.random.randint(low=0, high=len(colors))
    while (rand_num1 == rand_num2): # If num1 == num2 create new one until they different
        rand_num2 = np.random.randint(low=0, high=len(colors))
    
    if (rand_num1 > rand_num2):
        new_colors = new_colors[rand_num2::] + new_colors[rand_num2:rand_num1:-1] + new_colors[rand_num1::]


def solve_via_simulated_annealing(
    G: nx.Graph, n_max_colors: int, initial_colors: NDArrayInt, n_iters: int
):
    loss_history = np.zeros((n_iters,), dtype=np.int_)
    #n_tweaks = 10
    cur_colors = initial_colors
    #next_colors = initial_colors.copy()
    next_colors_best = initial_colors.copy()

    temperature = 2.5
    speed_of_cooling_down = 0.01
    arr_of_loss_history = []

    for i in range(n_iters):
        if(temperature != 0):
            loss_history[i] = number_of_conflicts(G, cur_colors)
            arr_of_loss_history.append(loss_history[i])
            next_colors_best = tweak(cur_colors, n_max_colors, G)
            
            cur_confl = number_of_conflicts(G, cur_colors)
            new_confl = number_of_conflicts(G, next_colors_best)
            delta_energy = new_confl - cur_confl
            if (delta_energy <= 0):
                cur_colors = next_colors_best
                #temperature -= speed_of_cooling_down
                temperature = temperature_changing(temperature=temperature, i=i)
                if (temperature == 0):
                    print(min(arr_of_loss_history))
                    break
                    #return loss_history
            else:
                probability = 1
                #np.exp((delta_energy * (-1)) / temperature)
                num = np.random.uniform(0, 1)
                #print(num)
                #temperature -= speed_of_cooling_down
                temperature = temperature_changing(temperature=temperature, i=i)
                if (num <= probability):
                    cur_colors = next_colors_best
                if (temperature == 0):
                    print(min(arr_of_loss_history))
                    break
                    #return loss_history
        print(min(arr_of_loss_history))
                 
    return loss_history
    

if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    G = nx.erdos_renyi_graph(n=100, p=0.05, seed=seed)
    #plot_graph(G)
    
    n_max_iters = 250
    n_max_colors = 3
    initial_colors = np.random.randint(low=0, high=n_max_colors - 1, size=len(G.nodes))

    loss_history = solve_via_simulated_annealing(
        G, n_max_colors, initial_colors, n_max_iters
    )
    plot_loss_history(loss_history)
