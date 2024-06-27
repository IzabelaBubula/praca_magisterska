import os
import tkinter
from datetime import datetime
from tkinter import *

import Grains
import ReadFile
import Show_plot
from Variables import Variables, get_structure, save_in_file

root = Tk()
t_1 = Text(root, wrap=WORD)


def create_folder():
    now = datetime.now()
    folder_name = now.strftime("%Y%m%d_%H%M")
    file_path = 'D:\\studia-II-stopnia\\sem 2\\metody_dyskretne\\projekt\\dane'
    results_path = 'D:\\studia-II-stopnia\\sem 2\\metody_dyskretne\\projekt\\wyniki'
    os.makedirs(file_path + "\\" + folder_name)
    os.makedirs(results_path + "\\" + folder_name)
    Variables.FOLDER_NAME = file_path + "\\" + folder_name
    Variables.RESULTS_FOLDER_NAME = results_path + "\\" + folder_name


def open_app():
    root.title('App')
    Variables.file_counter = 0

    # create_folder()
    moore = IntVar()
    von = IntVar()
    pre = IntVar()
    abs = IntVar()
    itera = IntVar()

    def click_action():
        Variables.num_iterations.append(itera.get())
        Variables.boundary_conditions.append('abs' if abs.get() == 1 else 'per')
        Variables.neighborhood.append('moore' if moore.get() == 1 else 'von')

    def click_action1():
        # ReadFile.choose_directory()
        # print(Variables.file_names)
        # for n in range(len(Variables.file_names)):
        options = []
        fileData = ReadFile.file_to_array(Variables.file_names[0])
        print("Start counting")
        structure = Grains.generate_initial_structure(fileData)
        fileNumber = 0
        structure = Grains.grow(structure, fileData, fileNumber)
        Variables.structure = structure
        open_show(options)

    def showThreeD():
        structure = Variables.structure
        Show_plot.threeDFigure(structure)

    def showGrid():
        structure = Variables.structure
        Show_plot.plot_2d_cuboid_mesh(structure)

    def open_show(options):
        new = Toplevel(root)
        new.geometry("750x250")
        new.title("Show plot")

        # number = StringVar()
        # number.set(options[0])

        # w = OptionMenu(new, number, *options)
        # w.pack()

        button = Button(new, text="Show 3D", command=lambda: showThreeD())
        button.pack()

        button = Button(new, text="Show grid", command=lambda: showGrid())
        button.pack()

        new.mainloop()


    tkinter.Label(root, text="Choose neighbourhood").grid(row=2, sticky=W)
    tkinter.Checkbutton(root, text="Moore", variable=moore, onvalue=1, offvalue=0).grid(row=3, column=0, sticky=W)
    tkinter.Checkbutton(root, text="Von Neumann", variable=von, onvalue=1, offvalue=0).grid(row=3, column=1, sticky=W)

    tkinter.Label(root, text="Choose boundary conditions").grid(row=4, sticky=W)
    tkinter.Checkbutton(root, text="Periodic", variable=pre, onvalue=1, offvalue=0).grid(row=5, column=0, sticky=W)
    tkinter.Checkbutton(root, text="Absorbing", variable=abs, onvalue=1, offvalue=0).grid(row=5, column=1, sticky=W)

    tkinter.Label(root, text='iterations:').grid(row=8, column=0, sticky=W)
    tkinter.Entry(root, textvariable=itera).grid(row=8, column=1, sticky=W)

    b_1 = Button(root, text="Open K Files", width=8, command=ReadFile.open_files)
    b_1.grid(row=12, column=4, sticky=W)

    b_1 = Button(root, text="Save data", width=8, command=lambda: click_action())
    b_1.grid(row=12, column=5, sticky=W)

    b_1 = Button(root, text="Count", width=8, command=lambda: click_action1())
    b_1.grid(row=12, column=6, sticky=W)

    root.mainloop()
