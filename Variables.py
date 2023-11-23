import os

from Read_file import read_input_file


class Variables:
    num_iterations = 0
    num_seeds = 0
    boundary_conditions = ""
    neighborhood = ""
    size_x: int = 0
    size_y = 0
    size_z = 0
    mc = 0
    FOLDER_NAME = ""
    file_counter = 0


    @classmethod
    def assign_the_variables(cls, filepath):
        file_path = filepath  # Replace with the actual file path
        input_params = read_input_file(file_path)

        cls.size_x = input_params['size x']
        cls.size_y = input_params['size y']
        cls.size_z = input_params['size z']
        cls.neighborhood = input_params['neighbourhood']
        cls.boundary_conditions = input_params['boundary conditions']
        cls.num_seeds = input_params['number of seeds']
        cls.num_iterations = input_params['number of iterations']
        cls.mc = input_params['monte_carlo']


def save_in_file():
    file_name = "variables_" + str(Variables.file_counter) + ".txt"
    file_path = Variables.FOLDER_NAME + "\\" + file_name
    with open(file_path, 'x') as file:
        file.write('size x : ' + str(Variables.size_x) + '\n')
        file.write('size y : ' + str(Variables.size_y) + '\n')
        file.write('size z : ' + str(Variables.size_z) + '\n')
        file.write('neighbourhood : ' + Variables.neighborhood + '\n')
        file.write('boundary conditions : ' + Variables.boundary_conditions + '\n')
        file.write('number of seeds : ' + str(Variables.num_seeds) + '\n')
        file.write('number of iterations: ' + str(Variables.num_iterations) + '\n')
        file.write('monte_carlo: ' + str(Variables.mc) + '\n')
    Variables.file_counter += 1

