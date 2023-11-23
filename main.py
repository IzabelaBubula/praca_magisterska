from tkinter import *

import Grains
import Show_plot
from App import open_app
from Variables import Variables


# Reading variables form file
Variables.assign_the_variables('D:\\studia-II-stopnia\\sem 2\\metody_dyskretne\\data.txt')

# Generating initial structure
structure = Grains.generate_initial_structure(Variables.size_x, Variables.size_y, Variables.size_z, Variables.num_seeds)

# Simulation of grain growth
structure = Grains.choose_grow(structure)

open_app(structure)