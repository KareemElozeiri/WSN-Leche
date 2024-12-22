from node import Node
import numpy as np 
import matplotlib.pyplot as plt
import pickle

def generate_topology(N, x1=0, x2=100, y1=0, y2=100):
    np.random.seed(70)
    potential_points = N**2
    X = np.linspace(x1, x2, potential_points)
    Y = np.linspace(y1, y2, potential_points)
    
    ind_x = np.random.choice(potential_points, size=N, replace=False)
    ind_y = np.random.choice(potential_points, size=N, replace=False)

    X = X[ind_x]
    Y = Y[ind_y]
    
    nodes = [Node(X[i], Y[i]) for i in range(len(X))]
    
    return nodes

def graph_topology(nodes, sink_x, sink_y,sim_case, energies = None, cycle=None):
    X_coords = [node.x for node in nodes]
    y_coords = [node.y for node in nodes]
    
    fig = plt.figure(figsize=(10,10))
    if energies is not None:
        # plt.figure(figsize=(10, 8))
        scatter = plt.scatter(X_coords, y_coords, c=energies, cmap='viridis', s=100, edgecolor='k')
        cbar = plt.colorbar(scatter)
        cbar.set_label('Energy')
    else:
        plt.scatter(X_coords,y_coords, label="sensor", marker='x')
        
    
    plt.scatter(sink_x, sink_y, cmap="red", label="Sink", marker='o', s=250)
    plt.xlim(0,100)
    if sim_case == 'Out':
        plt.ylim(0,250)
    else:
        plt.ylim(0,100)
    title = f'{sim_case} {"Energy" if energies is not None else ""} Network Topology {("after" + cycle) if cycle is not None else ""}'
    plt.title(title)

    # title = f'{sim_case}_Topology'
    
        
    plt.xlabel('X position (m)')
    plt.ylabel('Y position (m)')
    plt.legend()
    plt.show()
    # fig.savefig(f'Figures//{sim_case}//{title}.jpg')

    # with open(f'Figures//{sim_case}//{title}.fig', 'wb') as fig_file:
    #     pickle.dump(fig, fig_file)
def run_iteration(nodes, sink_x, sink_y, R=30, im_criteria= 'Given'):
    dead_count = []
    remaining_energies = []
                
    
    return dead_count, remaining_energies

def run_simulation(sink_x, sink_y, N_sensors,sim_case,R,im_criteria):
    nodes = generate_topology(N_sensors)
    graph_topology(nodes, sink_x, sink_y,sim_case)

    dead_counts = []
    energies = []
    
    while True:
        dead_count, curr_energies = run_iteration(nodes, sink_x, sink_y,R, im_criteria)
        dead_counts.append(dead_count)
        energies.append(curr_energies)

        if dead_count == len(nodes):
            break
    
    dead_counts = np.array(dead_counts)
    special_cycles = [(np.argmin(np.abs(dead_counts-x))) for x in [1,N_sensors/2,N_sensors]] #first, half, last
    special_values = len(nodes) - dead_counts[special_cycles] # Corresponding Values, Cuz they're not necessarily 1,50,100 (Maybe more than one died at the same cycled)
    
    return len(nodes) - np.array(dead_counts), np.array(energies)[special_cycles], np.array(special_cycles)+1, np.array(special_values),nodes
    # In the prev line, returned special_cycles + 1 , to start at cycle 1 not 0