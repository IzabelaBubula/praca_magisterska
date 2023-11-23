def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    params = {}

    for line in lines:
        if ':' in line:
            key, value = [item.strip() for item in line.split(':')]
            params[key] = int(value) if key != 'neighbourhood' and key != 'boundary conditions' else value

    return params
