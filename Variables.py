import os

import numpy as np


class Variables:
    num_iterations = []
    boundary_conditions = []
    neighborhood = []
    file_names = []
    save_directory_name = ""
    size_x = 11
    size_y = 11
    size_z = 3
    start_informations = []
    structure = [[[]]]


    # @classmethod
    # def assign_the_variables(cls, file_name):
    #     file_path = file_name # Replace with the actual file path
    #     input_params = read_input_file(file_path)
    #
    #     cls.neighborhood = input_params['neighbourhood']
    #     cls.boundary_conditions = input_params['boundary conditions']
    #     cls.num_seeds = input_params['number of seeds']
    #     cls.num_iterations = input_params['number of iterations']
    #     cls.mc = input_params['monte_carlo']


def save_in_file(fileNumber):
    file_name = "result_" + str(Variables.file_names[fileNumber]) + ".txt"
    file_path = Variables.save_directory_name + "\\" + file_name
    with open(file_path, 'x') as file:
        file.write('neighbourhood : ' + Variables.neighborhood + '\n')
        file.write('boundary conditions : ' + Variables.boundary_conditions + '\n')
        file.write('number of iterations: ' + str(Variables.num_iterations) + '\n')


def save_results(structure):
    file_name = "results" + str(Variables.result_counter) + ".txt"
    file_path = Variables.RESULTS_FOLDER_NAME + "\\" + file_name
    with open(file_path, 'x') as file:
        if Variables.mc == 0:
            file.write("CA simulation time: " + str(Variables.ca_time) + "\n")
        else:
            file.write("MC simulation time: " + str(Variables.mc_time) + "\n")
        file.write("x: " + str(Variables.size_x) + "\n")
        file.write("y: " + str(Variables.size_y) + "\n")
        file.write("z: " + str(Variables.size_z) + "\n")
        if Variables.size_z == 0:
            for i in range(Variables.size_x):
                for j in range(Variables.size_y):
                    file.write(str(i) + " " + str(j) + " " + str(structure[i][j]) + "\n")
        else:
            for i in range(Variables.size_x):
                for j in range(Variables.size_y):
                    for k in range(Variables.size_z):
                        file.write(str(i) + " " + str(j) + " " + str(k) + " " + str(structure[i][j][k]) + "\n")

    Variables.result_counter += 1


def get_structure(filename):
    file_path = Variables.RESULTS_FOLDER_NAME + "\\" + filename
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Extract sizes from the first three lines
        size_x = int(lines[1].split(":")[1].strip())
        size_y = int(lines[2].split(":")[1].strip())

        # Check if size_z is present and not zero
        size_z = int(lines[3].split(":")[1].strip())

        if size_z == 0:
            Variables.size_z = 0
            structure = np.zeros((size_x, size_y), dtype=int)
            i = 4
            for x in range(size_x):
                for y in range(size_y):
                    structure[x][y] = int(lines[i].split()[-1])
                    i += 1
        else:
            structure = np.zeros((size_x, size_y, size_z), dtype=int)
            Variables.size_z = size_z
            i = 4
            for x in range(size_x):
                for y in range(size_y):
                    for z in range(size_z):
                        structure[x][y][z] = int(lines[i].split()[-1])
                        i += 1

        return structure

