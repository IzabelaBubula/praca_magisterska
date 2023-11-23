from Read_file import read_input_file


class Variables:
    num_iterations = 0
    num_seeds = 0
    boundary_conditions = ""
    iteration_count = 0
    neighborhood = ""
    size_x: int = 0
    size_y = 0
    size_z = 0
    mc = 0

    @classmethod
    def assign_the_variables(cls, filepath):
        file_path = filepath  # Replace with the actual file path
        input_params = read_input_file(file_path)

        cls.size_x = input_params['size x']
        cls.size_y = input_params['size y']
        cls.size_z = input_params['size z']
        cls.neighborhood = input_params['neighbourhood']
        cls.iteration_count = input_params['iteration count']
        cls.boundary_conditions = input_params['boundary conditions']
        cls.num_seeds = input_params['number of seeds']
        cls.num_iterations = input_params['number of iterations']
        cls.mc = input_params['monte_carlo']
