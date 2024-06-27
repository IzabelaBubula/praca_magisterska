import numpy as np
from matplotlib import pyplot as plt

from Variables import Variables

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

def threeDFigure(structure):
    # Stworzenie figurki i dodanie wykresu 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Rozpakowanie wymiarów tablicy
    x = Variables.size_x
    y = Variables.size_y
    z = Variables.size_z

    # Tworzenie siatki współrzędnych
    x_vals, y_vals, z_vals = np.indices((x, y, z))

    # Przekształcenie współrzędnych i wartości do jednowymiarowych tablic
    x_vals = x_vals.flatten()
    y_vals = y_vals.flatten()
    z_vals = z_vals.flatten()
    structureToShow = np.array(structure);
    values = structureToShow.flatten()

    norm = plt.Normalize(values.min(), values.max())
    colors = plt.cm.viridis(norm(values))

    # Tworzenie wykresu scatter
    scatter = ax.scatter(x_vals, y_vals, z_vals, c=colors, marker='o', s=100)

    # Dodanie kolorowej legendy
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label('Wartości')

    ax.set_yticks(np.arange(0, y, 1))

    # Usunięcie linii osi i linii pomocniczych
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.grid(False)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # Usunięcie nazw osi
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')

    # Tytuł wykresu
    ax.set_title('Projekcja 3D')

    # Wyświetlenie wykresu
    plt.show()
