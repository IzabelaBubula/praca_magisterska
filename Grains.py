import random
import time

import numpy as np
import Neightbours
from Show_plot import plot_2d_cuboid_mesh, choose_plot
from Variables import Variables


def generate_initial_structure(size_x, size_y, size_z, num_seeds):

    numb = 1
    if size_z != 0:
        structure = np.zeros((size_x, size_y, size_z), dtype=int)
        seeds = random.sample(range(size_x * size_y * size_z), num_seeds)

        for seed in seeds:
            # Obliczenie współżęsnych komórek x, y i z
            x = seed // (size_y * size_z)
            y = (seed % (size_y * size_z)) // size_z
            z = (seed % (size_y * size_z)) % size_z
            structure[x, y, z] = numb  # Each seed has a unique identifier
            numb += 1
    elif size_z == 0:
        structure = np.zeros((size_x, size_y), dtype=int)
        seeds = random.sample(range(size_x * size_y), num_seeds)

        for seed in seeds:
            row = seed // size_x
            col = seed % size_y
            structure[row, col] = seed + 1  # Each seed has a unique identifier

    return structure


def choose_grow(structure):
    if Variables.mc == 1:
        return monte_carlo_grain_growth()
    else:
        for _ in range(Variables.num_iterations):
            structure = grow_grains(structure, Variables.size_x, Variables.size_y, Variables.size_z)
        return structure


def grow_grains(structure, size_x, size_y, size_z):
    start_time = time.time()
    new_structure = np.copy(structure)

    for row in range(size_x):
        for col in range(size_y):
            if size_z == 0:
                if structure[row, col] == 0:
                    neighbors = Neightbours.choose_neighbour_2(row, col, size_x, size_y)

                    neighbor_values = [structure[n_row, n_col] for n_row, n_col in neighbors if
                                       structure[n_row, n_col] != 0]

                    if neighbor_values:
                        dominant_value = max(set(neighbor_values), key=neighbor_values.count)
                        new_structure[row, col] = dominant_value
            elif size_z != 0:
                for wid in range(size_z):
                    if structure[row, col, wid] == 0:
                        neighbors = Neightbours.choose_neighbour_3(row, col, wid, size_x, size_y, size_z)

                        # Algorytm rozrostu ziaren dla komórki
                        neighbor_values = [structure[n_row, n_col, n_wid] for n_row, n_col, n_wid in neighbors if
                                           structure[n_row, n_col, n_wid] != 0]

                        if neighbor_values:
                            dominant_value = max(set(neighbor_values), key=neighbor_values.count)
                            new_structure[row, col, wid] = dominant_value

    end_time = time.time()
    Variables.sim_time = end_time - start_time
    return new_structure


def setup_montecarlo():

    if Variables.size_z != 0:
        structure = np.zeros((Variables.size_x, Variables.size_y, Variables.size_z), dtype=int)
        for i in range(Variables.size_x):
            for j in range(Variables.size_y):
                for k in range(Variables.size_z):
                    structure[i][j][k] = np.random.randint(Variables.num_seeds)
    else:
        structure = np.zeros((Variables.size_x, Variables.size_y), dtype=int)
        for j in range(Variables.size_x):
            for k in range(Variables.size_y):
                structure[j][k] = np.random.randint(Variables.num_seeds)
    return structure


def monte_carlo_grain_growth():
    if Variables.size_z == 0:
        newmc = setup_montecarlo()

        for _ in range(Variables.num_iterations):
            row = random.randint(0, Variables.size_x - 1)
            col = random.randint(0, Variables.size_y - 1)
            if calculate_energy(newmc, row, col):
                newmc[row, col] = newmc[row][col] + 1
        return newmc
    else:
        newmc = setup_montecarlo()

        for _ in range(Variables.num_iterations):
            row = random.randint(0, Variables.size_x - 1)
            col = random.randint(0, Variables.size_y - 1)
            wid = random.randint(0, Variables.size_z - 1)
            if calculate_energy_3(newmc, row, col, wid):
                newmc[row, col, wid] = newmc[row][col][wid] + 1
        return newmc


def calculate_energy(structure, row, col):
    different_energy_neighbors = []
    neighbors = Neightbours.choose_neighbour_2(row, col, Variables.size_x, Variables.size_y)
    for n in neighbors:
        if structure[row][col] != structure[n[0]][n[1]]:
            different_energy_neighbors.append(n)
    return len(different_energy_neighbors) >= len(neighbors) / 3


def calculate_energy_3(structure, row, col, wid):
    different_energy_neighbors = []
    neighbors = Neightbours.choose_neighbour_3(row, col, wid, Variables.size_x, Variables.size_y, Variables.size_z)
    for n in neighbors:
        if structure[row][col][wid] != structure[n[0]][n[1]][n[2]]:
            different_energy_neighbors.append(n)
    return len(different_energy_neighbors) >= len(neighbors) / 3







