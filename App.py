import os
import tkinter
from datetime import datetime
from tkinter import *

import Show_plot

root = Tk()
t_1 = Text(root, wrap=WORD)

def create_folder():
    now = datetime.now()
    folder_name = now.strftime("%Y%m%d_%H%M")
    file_path = 'D:\studia-II-stopnia\sem 2\metody_dyskretne\projekt\dane'
    os.makedirs(file_path)
    return file_path+"\ " + folder_name

# def save_variables(path):
    

def open_app(structure):
    root.title('App')

    create_folder()

    two = IntVar()
    three = IntVar()
    moore = IntVar()
    von = IntVar()
    pre = IntVar()
    abs = IntVar()
    aut = IntVar()
    mc = IntVar()

    tkinter.Label(root, text="Choose dimension").grid(row=0, sticky=W)
    tkinter.Checkbutton(root, text="2D", variable=two, onvalue=1, offvalue=0).grid(row=1, column=0, sticky=W)
    tkinter.Checkbutton(root, text="3D", variable=three, onvalue=1, offvalue=0).grid(row=1, column=1, sticky=W)

    tkinter.Label(root, text="Choose neighbourhood").grid(row=2, sticky=W)
    tkinter.Checkbutton(root, text="Moore", variable=moore, onvalue=1, offvalue=0).grid(row=3, column=0, sticky=W)
    tkinter.Checkbutton(root, text="Von Neumann", variable=von, onvalue=1, offvalue=0).grid(row=3, column=1, sticky=W)

    tkinter.Label(root, text="Choose boundary conditions").grid(row=4, sticky=W)
    tkinter.Checkbutton(root, text="Periodic", variable=pre, onvalue=1, offvalue=0).grid(row=5, column=0, sticky=W)
    tkinter.Checkbutton(root, text="Absorbing", variable=abs, onvalue=1, offvalue=0).grid(row=5, column=1, sticky=W)

    tkinter.Label(root, text="x size:").grid(row=7, column=0, sticky=W)
    x_val = tkinter.Entry(root).grid(row=7, column=1, sticky=W)

    tkinter.Label(root, text="y size:").grid(row=7, column=2, sticky=W)
    y_val = tkinter.Entry(root).grid(row=7, column=3, sticky=W)

    tkinter.Label(root, text="z size:").grid(row=7, column=4, sticky=W)
    z_val = tkinter.Entry(root).grid(row=7, column=5, sticky=W)

    tkinter.Label(root, text='iterations:').grid(row=8, column=0, sticky=W)
    iter = tkinter.Entry(root).grid(row=8, column=1, sticky=W)

    tkinter.Label(root, text='nuber of seeds:').grid(row=9, column=0, sticky=W)
    nrsee = tkinter.Entry(root).grid(row=9, column=1, sticky=W)

    tkinter.Label(root, text="Choose growth").grid(row=10, sticky=W)
    tkinter.Checkbutton(root, text="MonteCarlo", variable=mc, onvalue=1, offvalue=0).grid(row=11, column=0, sticky=W)
    tkinter.Checkbutton(root, text="Automations", variable=aut, onvalue=1, offvalue=0).grid(row=11, column=1, sticky=W)

    b_1 = Button(root, text="Show", width=8, command=lambda: click_action(two, three, moore, von, abs, pre, mc, aut, x_val, y_val, z_val, iter, nrsee))

    root.mainloop()
