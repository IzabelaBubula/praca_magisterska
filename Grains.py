import random
import time

import numpy as np
import Neightbours
from Variables import Variables


#sekwencyjne
#zrwnoleglenie
#testy wydajnociowe

def generate_initial_structure(size_x, size_y, size_z, num_seeds):
    numb = 1
    if size_z != 0:
        structure = np.zeros((size_x, size_y, size_z), dtype=int)
        seeds = random.sample(range(size_x * size_y * size_z), num_seeds)

        for seed in seeds:
            # Obliczenie współżęsnych komórek x, y i z
            x = seed // (size_y * size_z)
            y = (seed % (size_y * size_z))// size_z
            z = (seed % (size_y * size_z)) % size_z
            structure[x, y, z] = numb  # Each seed has a unique identifier
            numb += 1
    elif size_z == 0:
        structure = np.zeros((size_x, size_y), dtype=int)
        seeds = random.sample(range(size_x * size_y), num_seeds)

        for seed in seeds:
            row = seed // size_x
            col = seed % size_y
            structure[row, col] = numb # Each seed has a unique identifier
            numb += 1

    return structure


def choose_grow(structure):
    if Variables.mc == 1:
        start_montecarlo = time.time()
        for _ in range(Variables.num_iterations):
            structure = monte_carlo_grain_growth(structure, Variables.size_x, Variables.size_y, Variables.size_z)
        end_montecarlo = time.time()
        Variables.mc_time = end_montecarlo - start_montecarlo
        print(str(Variables.mc_time))
        return structure
    else:
        start_ca = time.time()
        while 0 in structure:
            structure = grow_grains(structure, Variables.size_x, Variables.size_y, Variables.size_z)
        end_ca = time.time()
        Variables.ca_time = end_ca - start_ca
        print(str(Variables.ca_time))
        return structure


def grow_grains(structure, size_x, size_y, size_z):
    new_structure = np.copy(structure)

    for row in range(size_x):
        for col in range(size_y):
            if size_z == 0:
                if new_structure[row, col] == 0:
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

                        neighbor_values = [structure[n_row, n_col, n_wid] for n_row, n_col, n_wid in neighbors if
                                           structure[n_row, n_col, n_wid] != 0]

                        if neighbor_values:
                            dominant_value = max(set(neighbor_values), key=neighbor_values.count)
                            new_structure[row, col, wid] = dominant_value
    return new_structure


def monte_carlo_grain_growth(structure, size_x, size_y, size_z):
    if Variables.size_z == 0:
        for row in range(size_x):
            for col in range(size_y):
                now_ener = calculate_energy(structure, row, col)
                nv = random.randint(0, Variables.num_seeds)

                structure[row, col] = nv
                new_ener = calculate_energy(structure, row, col)

                ener_change = new_ener - now_ener

                if ener_change > 0:
                    prop = random.random()
                    if prop > 0.5:
                        structure[row, col] = now_ener

        return structure
    else:
        for row in range(size_x):
            for col in range(size_y):
                for wid in range(size_z):
                    now_ener = calculate_energy_3(structure, row, col, wid)
                    nv = random.randint(0, Variables.num_seeds)

                    structure[row, col, wid] = nv
                    new_ener = calculate_energy_3(structure, row, col, wid)

                    ener_change = new_ener - now_ener

                    if ener_change > 0:
                        prop = random.random()
                        if prop > 0.5:
                            structure[row, col, wid] = now_ener
        return structure


def calculate_energy(structure, row, col):
    current_value = structure[row, col]
    neighbors = Neightbours.choose_neighbour_2(row, col, Variables.size_x, Variables.size_y)

    different_energy_neighbors = 0

    for neighbor in neighbors:
        n_row, n_col = neighbor
        if structure[n_row][n_col] != current_value:
            different_energy_neighbors += 1

    return different_energy_neighbors


def calculate_energy_3(structure, row, col, wid):
    current_value = structure[row, col, wid]
    neighbors = Neightbours.choose_neighbour_3(row, col, wid, Variables.size_x, Variables.size_y, Variables.size_z)

    different_energy_neighbors = 0

    for neighbor in neighbors:
        n_row, n_col, n_wid = neighbor
        if structure[n_row][n_col][n_wid] != current_value:
            different_energy_neighbors += 1

    return different_energy_neighbors
