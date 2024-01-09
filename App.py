import os
import tkinter
from datetime import datetime
from tkinter import *

import Grains
import Show_plot
from Variables import Variables, save_in_file, save_results, get_structure


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

    create_folder()
    moore = IntVar()
    von = IntVar()
    pre = IntVar()
    abs = IntVar()
    aut = IntVar()
    mc = IntVar()
    x_val = IntVar()
    y_val = IntVar()
    z_val = IntVar()
    itera = IntVar()
    seed = IntVar()

    def click_action():
        Variables.size_x = x_val.get()
        Variables.size_y = y_val.get()
        Variables.size_z = z_val.get()
        Variables.num_seeds = seed.get()
        Variables.num_iterations = itera.get()
        Variables.boundary_conditions = 'abs' if abs.get() == 1 else 'per'
        Variables.mc = 1 if mc.get() == 1 else 0
        Variables.neighborhood = 'moore' if moore.get() == 1 else 'von'

        save_in_file()

    def click_action1():
        counter = 0
        options = []
        while Variables.file_counter > counter:
            file_name = "variables_" + str(counter) + ".txt"
            options.append("results" + str(counter) + ".txt")
            Variables.assign_the_variables(Variables.FOLDER_NAME + "\\" + file_name)
            structure = Grains.generate_initial_structure(Variables.size_x, Variables.size_y, Variables.size_z,
                                                          Variables.num_seeds)
            structure = Grains.choose_grow(structure)
            counter += 1
            save_results(structure)
        open_new(options)

    def open_new(options):
        new = Toplevel(root)
        new.geometry("750x250")
        new.title("Show plot")

        number = StringVar()
        number.set(options[0])

        w = OptionMenu(new, number, *options)
        w.pack()

        def choose():
            structure = get_structure(number.get())
            Show_plot.choose_plot(structure)

        button = Button(new, text="choose file to show", command=choose)
        button.pack()

        new.mainloop()

    tkinter.Label(root, text="Choose neighbourhood").grid(row=2, sticky=W)
    tkinter.Checkbutton(root, text="Moore", variable=moore, onvalue=1, offvalue=0).grid(row=3, column=0, sticky=W)
    tkinter.Checkbutton(root, text="Von Neumann", variable=von, onvalue=1, offvalue=0).grid(row=3, column=1, sticky=W)

    tkinter.Label(root, text="Choose boundary conditions").grid(row=4, sticky=W)
    tkinter.Checkbutton(root, text="Periodic", variable=pre, onvalue=1, offvalue=0).grid(row=5, column=0, sticky=W)
    tkinter.Checkbutton(root, text="Absorbing", variable=abs, onvalue=1, offvalue=0).grid(row=5, column=1, sticky=W)

    tkinter.Label(root, text="x size:").grid(row=7, column=0, sticky=W)
    tkinter.Entry(root, textvariable=x_val).grid(row=7, column=1, sticky=W)

    tkinter.Label(root, text="y size:").grid(row=7, column=2, sticky=W)
    tkinter.Entry(root, textvariable=y_val).grid(row=7, column=3, sticky=W)

    tkinter.Label(root, text="z size:").grid(row=7, column=4, sticky=W)
    tkinter.Entry(root, textvariable=z_val).grid(row=7, column=5, sticky=W)

    tkinter.Label(root, text='iterations:').grid(row=8, column=0, sticky=W)
    tkinter.Entry(root, textvariable=itera).grid(row=8, column=1, sticky=W)

    tkinter.Label(root, text='nuber of seeds:').grid(row=9, column=0, sticky=W)
    tkinter.Entry(root, textvariable=seed).grid(row=9, column=1, sticky=W)

    tkinter.Label(root, text="Choose growth").grid(row=10, sticky=W)
    tkinter.Checkbutton(root, text="MonteCarlo", variable=mc, onvalue=1, offvalue=0).grid(row=11, column=0, sticky=W)
    tkinter.Checkbutton(root, text="Automations", variable=aut, onvalue=1, offvalue=0).grid(row=11, column=1, sticky=W)

    b_1 = Button(root, text="Save data", width=8, command=lambda: click_action())
    b_1.grid(row=12, column=4, sticky=W)

    b_1 = Button(root, text="Count", width=8, command=lambda: click_action1())
    b_1.grid(row=12, column=5, sticky=W)

    root.mainloop()
