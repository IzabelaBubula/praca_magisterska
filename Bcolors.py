class Bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'


def print_matrix(structure, size_x, size_y):
    for i in range(size_x):
        for j in range(size_y):
            if structure[i][j] == 1:
                print(Bcolors.WARNING + str(structure[i][j]) + Bcolors.ENDC, end='  ')
            if structure[i][j] == 2:
                print(Bcolors.OKGREEN + str(structure[i][j]) + Bcolors.ENDC, end='  ')
            if structure[i][j] == 0:
                print(str(0), end='  ')
        print("\n")
