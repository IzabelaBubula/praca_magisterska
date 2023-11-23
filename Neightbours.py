from Cell import Cell
from Variables import Variables


def choose_neighbour_2(row, col, size_x, size_y):
    nb = Variables.neighborhood
    bc = Variables.boundary_conditions

    neighbor = []
    if nb == "moore":
        if bc == "abs":
            neighbor = get_neighbors_absorbing_moore(row, col, size_x, size_y)
        elif bc == "per":
            neighbor = get_neighbors_periodic(row, col, size_x, size_y)
    elif nb == "von":
        if bc == "abs":
            neighbor = get_neighbors_absorbing_von_neumann(row, col, size_x, size_y)
        elif bc == "per":
            neighbor = get_neighbors_periodic_von(row, col, size_x, size_y)
            i = 0

    return neighbor


def choose_neighbour_3(row, col, wid, size_x, size_y, size_z):
    nb = Variables.neighborhood
    bc = Variables.boundary_conditions

    neighbor = []
    if nb == "moore":
        if bc == "abs":
            neighbor = get_neighbors_absorbing_moore_3d(row, col, wid, size_x, size_y, size_z)
        elif bc == "per":
            neighbor = get_neighbors_periodic_3d(row, col, wid, size_x, size_y, size_z)
    elif nb == "von":
        if bc == "abs":
            neighbor = get_neighbors_absorbing_von_neumann_3d(row, col, wid, size_x, size_y, size_z)
        elif bc == "per":
            neighbor = get_neighbors_periodic_von_3d(row, col, wid, size_x, size_y, size_z)

    return neighbor

# 2D
# periodicity


def get_neighbors_periodic(row, col, size_x, size_y):
    neighbors = []

    # Sąsiedztwo wertykalne
    neighbor_up = (row - 1) % size_x
    neighbor_down = (row + 1) % size_x
    neighbors.append((neighbor_up, col))
    neighbors.append((neighbor_down, col))

    # Sąsiedztwo pionowe
    neighbor_left = (col - 1) % size_y
    neighbor_right = (col + 1) % size_y
    neighbors.append((row, neighbor_left))
    neighbors.append((row, neighbor_right))

    # Sąsiedztwo po przekątnej
    neighbors.append((neighbor_up, neighbor_left))
    neighbors.append((neighbor_up, neighbor_right))
    neighbors.append((neighbor_down, neighbor_left))
    neighbors.append((neighbor_down, neighbor_right))

    return neighbors


def get_neighbors_periodic_von(row, col, size_x, size_y):
    neighbors = []

    # Sąsiedztwo wertykalne z uwzględnieniem periodycznych warunków brzegowych
    neighbors.append(((row - 1) % size_x, col))
    neighbors.append(((row + 1) % size_x, col))

    # Sąsiedztwo pionowe z uwzględnieniem periodycznych warunków brzegowych
    neighbors.append((row, (col - 1) % size_y))
    neighbors.append((row, (col + 1) % size_y))

    return neighbors


def get_neighbors_absorbing_von_neumann(row, col, size_x, size_y):
    neighbors = []

    # Sąsiedztwo wertykalne z uwzględnieniem absorbujących warunków brzegowych
    if row - 1 >= 0:
        neighbors.append((row - 1, col))
    if row + 1 < size_y:
        neighbors.append((row + 1, col))

    # Sąsiedztwo pionowe z uwzględnieniem absorbujących warunków brzegowych
    if col - 1 >= 0:
        neighbors.append((row, col - 1))
    if col + 1 < size_x:
        neighbors.append((row, col + 1))

    return neighbors


def get_neighbors_absorbing_moore(row, col, size_x, size_y):
    neighbors = []

    # Sąsiedztwo wertykalne z uwzględnieniem absorbujących warunków brzegowych
    if row - 1 >= 0:
        neighbors.append((row - 1, col))
    if row + 1 < size_y:
        neighbors.append((row + 1, col))

    # Sąsiedztwo pionowe z uwzględnieniem absorbujących warunków brzegowych
    if col - 1 >= 0:
        neighbors.append((row, col - 1))
    if col + 1 < size_x:
        neighbors.append((row, col + 1))

    # Sąsiedztwo po przekątnej z uwzględnieniem absorbujących warunków brzegowych
    if row - 1 >= 0 and col - 1 >= 0:
        neighbors.append((row - 1, col - 1))
    if row - 1 >= 0 and col + 1 < size_x:
        neighbors.append((row - 1, col + 1))
    if row + 1 < size_y and col - 1 >= 0:
        neighbors.append((row + 1, col - 1))
    if row + 1 < size_y and col + 1 < size_x:
        neighbors.append((row + 1, col + 1))

    return neighbors


# 3D


def get_neighbors_periodic_3d(row, col, wid, size_x, size_y, size_z):
    neighbors = []

    # Sąsiedztwo wertykalne z uwzględnieniem periodycznych warunków brzegowych
    neighbor_up = (row - 1) % size_x  # down
    neighbor_down = (row + 1) % size_x  # up
    neighbors.append((neighbor_up, col, wid))
    neighbors.append((neighbor_down, col, wid))

    # Sąsiedztwo pionowe z uwzględnieniem periodycznych warunków brzegowych
    neighbor_left = (col - 1) % size_y
    neighbor_right = (col + 1) % size_y
    neighbors.append((row, neighbor_left, wid))
    neighbors.append((row, neighbor_right, wid))

    # Sąsiedztwo w głąb i na powierzchni z uwzględnieniem periodycznych warunków brzegowych
    neighbor_front = (wid - 1) % size_z
    neighbor_back = (wid + 1) % size_z
    neighbors.append((row, col, neighbor_front))
    neighbors.append((row, col, neighbor_back))

    # Sąsiedztwo po przekątnej w płaszczyźnie xy z uwzględnieniem periodycznych warunków brzegowych
    neighbors.append((neighbor_up, neighbor_left, wid))
    neighbors.append((neighbor_up, neighbor_right, wid))
    neighbors.append((neighbor_down, neighbor_left, wid))
    neighbors.append((neighbor_down, neighbor_right, wid))

    # Sąsiedztwo po przekątnej w płaszczyźnie xz z uwzględnieniem periodycznych warunków brzegowych
    neighbors.append((neighbor_up, col, neighbor_front))
    neighbors.append((neighbor_up, col, neighbor_back))
    neighbors.append((neighbor_down, col, neighbor_front))
    neighbors.append((neighbor_down, col, neighbor_back))

    # Sąsiedztwo po przekątnej w płaszczyźnie yz z uwzględnieniem periodycznych warunków brzegowych
    neighbors.append((row, neighbor_left, neighbor_front))
    neighbors.append((row, neighbor_left, neighbor_back))
    neighbors.append((row, neighbor_right, neighbor_front))
    neighbors.append((row, neighbor_right, neighbor_back))

    return neighbors


def get_neighbors_periodic_von_3d(row, col, wid, size_x, size_y, size_z):
    neighbors = []

    # Sąsiedztwo wertykalne z uwzględnieniem periodycznych warunków brzegowych
    neighbors.append(((row - 1) % size_x, col, wid))
    neighbors.append(((row + 1) % size_x, col, wid))

    # Sąsiedztwo pionowe z uwzględnieniem periodycznych warunków brzegowych
    neighbors.append((row, (col - 1) % size_y, wid))
    neighbors.append((row, (col + 1) % size_y, wid))

    # Sąsiedztwo w głąb i na powierzchni z uwzględnieniem periodycznych warunków brzegowych
    neighbors.append((row, col, (wid - 1) % size_z))
    neighbors.append((row, col, (wid + 1) % size_z))

    return neighbors


def get_neighbors_absorbing_von_neumann_3d(row, col, wid, size_x, size_y, size_z):
    neighbors = []

    # Sąsiedztwo wertykalne z uwzględnieniem absorbujących warunków brzegowych
    if row - 1 >= 0:
        neighbors.append((row - 1, col, wid))
    if row + 1 < size_y:
        neighbors.append((row + 1, col, wid))

    # Sąsiedztwo pionowe z uwzględnieniem absorbujących warunków brzegowych
    if col - 1 >= 0:
        neighbors.append((row, col - 1, wid))
    if col + 1 < size_x:
        neighbors.append((row, col + 1, wid))

    # Sąsiedztwo w głąb i na powierzchni z uwzględnieniem absorbujących warunków brzegowych
    if wid - 1 >= 0:
        neighbors.append((row, col, wid - 1))
    if wid + 1 < size_z:
        neighbors.append((row, col, wid + 1))

    return neighbors


def get_neighbors_absorbing_moore_3d(row, col, wid, size_x, size_y, size_z):
    neighbors = []

    # Sąsiedztwo wertykalne z uwzględnieniem absorbujących warunków brzegowych
    if row - 1 >= 0:
        neighbors.append((row - 1, col, wid))
    if row + 1 < size_y:
        neighbors.append((row + 1, col, wid))

    # Sąsiedztwo pionowe z uwzględnieniem absorbujących warunków brzegowych
    if col - 1 >= 0:
        neighbors.append((row, col - 1, wid))
    if col + 1 < size_x:
        neighbors.append((row, col + 1, wid))

    # Sąsiedztwo w głąb i na powierzchni z uwzględnieniem absorbujących warunków brzegowych
    if wid - 1 >= 0:
        neighbors.append((row, col, wid - 1))
    if wid + 1 < size_z:
        neighbors.append((row, col, wid + 1))

    # Sąsiedztwo po przekątnej z uwzględnieniem absorbujących warunków brzegowych
    if row - 1 >= 0 and col - 1 >= 0:
        neighbors.append((row - 1, col - 1, wid))
    if row - 1 >= 0 and col + 1 < size_x:
        neighbors.append((row - 1, col + 1, wid))
    if row + 1 < size_y and col - 1 >= 0:
        neighbors.append((row + 1, col - 1, wid))
    if row + 1 < size_y and col + 1 < size_x:
        neighbors.append((row + 1, col + 1, wid))

    return neighbors

