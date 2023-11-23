import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from Variables import Variables


def choose_plot(structure):
    if Variables.size_z != 0:
        plot_2d_cuboid_mesh(structure)
    elif Variables.size_z == 0:
        plot_structure(structure)

def plot_structure(structure):
    plt.imshow(structure, cmap='viridis')
    plt.show()


def convert_to_array(structure, size_x):
    energy_array = np.zeros((size_x))
    for col in range(size_x):
        energy_array[col] = structure[col].q
    plot_structure(energy_array)


def get_top(structure):
    numbers = [[0 for _ in range(Variables.size_x)] for _ in range(Variables.size_z)]
    for i in range(Variables.size_x):
        for j in range(Variables.size_z):
            numbers[j][i] = structure[i][Variables.size_y - 1][j]
    return numbers


def get_bottom(structure):
    numbers = [[0 for _ in range(Variables.size_x)] for _ in range(Variables.size_z)]
    for i in range(Variables.size_x):
        for j in range(Variables.size_z):
            numbers[j][i] = structure[i][0][j]
    return numbers


def get_left(structure):
    numbers = [[0 for _ in range(Variables.size_z)] for _ in range(Variables.size_y)]
    for i in range(Variables.size_y):
        for j in range(Variables.size_z):
            numbers[i][j] = structure[Variables.size_x - 1][i][j]
    return numbers


def get_right(structure):
    numbers = [[0 for _ in range(Variables.size_z)] for _ in range(Variables.size_y)]
    for i in range(Variables.size_y):
        for j in range(Variables.size_z):
            numbers[i][j] = structure[0][i][j]
    return numbers

def get_front(structure):
    numbers = [[0 for _ in range(Variables.size_x)] for _ in range(Variables.size_y)]
    for i in range(Variables.size_x):
        for j in range(Variables.size_y):
            numbers[j][i] = structure[i][j][0]
    return numbers

def get_back(structure):
    numbers = [[0 for _ in range(Variables.size_x)] for _ in range(Variables.size_y)]
    for i in range(Variables.size_x):
        for j in range(Variables.size_y):
            numbers[j][i] = structure[i][j][Variables.size_z - 1]
    return numbers

def plot_2d_cuboid_mesh(structure):
    fig = plt.figure(figsize=(4, 5))
    row = 4
    col = 3

    fig.add_subplot(row,col,2)
    plt.imshow(get_back(structure), cmap='viridis')
    plt.axis('off')

    fig.add_subplot(row,col,5)
    plt.imshow(get_top(structure), cmap='viridis')
    plt.axis('off')

    fig.add_subplot(row, col, 7)
    plt.imshow(get_right(structure), cmap='viridis')
    plt.axis('off')

    fig.add_subplot(row, col, 8)
    plt.imshow(get_front(structure), cmap='viridis')
    plt.axis('off')

    fig.add_subplot(row, col, 9)
    plt.imshow(get_left(structure), cmap='viridis')
    plt.axis('off')

    fig.add_subplot(row, col, 11)
    plt.imshow(get_bottom(structure), cmap='viridis')
    plt.axis('off')

    plt.show()
