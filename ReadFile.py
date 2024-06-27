from tkinter import filedialog

from Variables import Variables


def open_files():
    file_paths = filedialog.askopenfilenames(
        title="Select K Files",
        filetypes=[("K files", "*.k"), ("All files", "*.*")]
    )
    Variables.file_names = file_paths

def choose_directory():
    directory_path = filedialog.askdirectory(
        title="Select save directory"
    )
    Variables.save_directory_name = directory_path


def file_to_array(file_path):
    data_array = []

    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into values
            values = line.strip().split(', ')

            if len(values) > 1:
                # Convert relevant values to floats, additionally multiplying by 100 the data is in form "0.00200"
                # for a point 2
                second_value = float(values[1])
                third_value = float(values[2])
                fourth_value = float(values[3])
                fifth_value = float(values[4])

                # Append the values to the data array
                data_array.append([int(second_value * 1000), int(third_value * 1000), int(fourth_value * 1000), fifth_value])
    return data_array
