import math
import random

import numpy as np

import Neightbours
from Variables import Variables
import pyopencl as cl

def generate_initial_structure(fileData):
    size_x = Variables.size_x
    size_y = Variables.size_y
    size_z = Variables.size_z
    structure = [[[0 for _ in range(size_z)] for _ in range(size_y)] for _ in range(size_x)]
    for f in fileData:
        structure[f[0]][f[1]][f[2]] = f[3]
    return structure

def grow(structure, grain_list, fileNumber):
    for _ in range(Variables.num_iterations[fileNumber]):
        structure = monte_carlo_grain_growth_opencl(structure, grain_list, fileNumber)
    return structure


def monte_carlo_grain_growth_opencl(structure, grain_list, fileNumber):
    # Create OpenCL context and queue
    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    context = cl.Context([device])
    queue = cl.CommandQueue(context)

    # Prepare the data
    size_x = Variables.size_x
    size_y = Variables.size_y
    size_z = Variables.size_z
    structure_np = np.array(structure, dtype=np.int32).flatten()
    grain_list_np = np.array(grain_list, dtype=np.int32).flatten()

    # Allocate GPU memory
    mf = cl.mem_flags
    structure_buf = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=structure_np)
    grain_list_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=grain_list_np)

    # OpenCL kernel code
    kernel_code = """
            __kernel void grain_growth(
                __global int* structure,
                const unsigned int size_x,
                const unsigned int size_y,
                const unsigned int size_z,
                const unsigned int neighborhood_type,
                const unsigned int boundary_condition
            ) {
                int index = get_global_id(0);
                if (structure[index] == 0) return;
                printf("index: %d", index);

                int x = index % size_x;
                int y = (index / size_x) % size_y;
                int z = index / (size_x * size_y);

                int neighbors[26][3];
                int num_neighbors = 0;

                // Select neighbors based on the neighborhood and boundary conditions
                if (neighborhood_type == 0) {  // Moore
                    if (boundary_condition == 0) {  // Absorbing
                        // Absorbing Moore neighborhood
                        if (x > 0) { neighbors[num_neighbors][0] = x - 1; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z; num_neighbors++; }
                        if (x < size_x - 1) { neighbors[num_neighbors][0] = x + 1; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z; num_neighbors++; }
                        if (y > 0) { neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y - 1; neighbors[num_neighbors][2] = z; num_neighbors++; }
                        if (y < size_y - 1) { neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y + 1; neighbors[num_neighbors][2] = z; num_neighbors++; }
                        if (z > 0) { neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z - 1; num_neighbors++; }
                        if (z < size_z - 1) { neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z + 1; num_neighbors++; }
                    } else {  // Periodic
                        // Periodic Moore neighborhood
                        neighbors[num_neighbors][0] = (x - 1 + size_x) % size_x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z; num_neighbors++;
                        neighbors[num_neighbors][0] = (x + 1) % size_x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z; num_neighbors++;
                        neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = (y - 1 + size_y) % size_y; neighbors[num_neighbors][2] = z; num_neighbors++;
                        neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = (y + 1) % size_y; neighbors[num_neighbors][2] = z; num_neighbors++;
                        neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = (z - 1 + size_z) % size_z; num_neighbors++;
                        neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = (z + 1) % size_z; num_neighbors++;
                    }
                } else {  // von Neumann
                    if (boundary_condition == 0) {  // Absorbing
                        // Absorbing von Neumann neighborhood
                        if (x > 0) { neighbors[num_neighbors][0] = x - 1; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z; num_neighbors++; }
                        if (x < size_x - 1) { neighbors[num_neighbors][0] = x + 1; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z; num_neighbors++; }
                        if (y > 0) { neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y - 1; neighbors[num_neighbors][2] = z; num_neighbors++; }
                        if (y < size_y - 1) { neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y + 1; neighbors[num_neighbors][2] = z; num_neighbors++; }
                        if (z > 0) { neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z - 1; num_neighbors++; }
                        if (z < size_z - 1) { neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z + 1; num_neighbors++; }
                    } else {  // Periodic
                        // Periodic von Neumann neighborhood
                        neighbors[num_neighbors][0] = (x - 1 + size_x) % size_x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z; num_neighbors++;
                        neighbors[num_neighbors][0] = (x + 1) % size_x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = z; num_neighbors++;
                        neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = (y - 1 + size_y) % size_y; neighbors[num_neighbors][2] = z; num_neighbors++;
                        neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = (y + 1) % size_y; neighbors[num_neighbors][2] = z; num_neighbors++;
                        neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = (z - 1 + size_z) % size_z; num_neighbors++;
                        neighbors[num_neighbors][0] = x; neighbors[num_neighbors][1] = y; neighbors[num_neighbors][2] = (z + 1) % size_z; num_neighbors++;
                    }
                }

                // Simple linear congruential generator (LCG) for random number generation
                uint seed = (index + 1) * 123456789;
                seed = (1103515245 * seed + 12345) % 2147483648;
                float rand_val = seed / 2147483648.0f;

                // Random choice and grain growth logic
                int rand_index = (int)(rand_val * num_neighbors);
                int nx = neighbors[rand_index][0];
                int ny = neighbors[rand_index][1];
                int nz = neighbors[rand_index][2];
                int neighbor_index = nz * size_x * size_y + ny * size_x + nx;
                
                printf("index %d, neig_index: %d", index, neighbor_index);

                if (structure[neighbor_index] == 0) {
                    float delta_energy = 1.0f;
                    float probability = exp(-delta_energy / structure[index]);
                    if (rand_val < probability) {
                        structure[neighbor_index] = structure[index];
                    }
                }
            }
            """

    # Compile the kernel
    program = cl.Program(context, kernel_code).build()

    # Kernel execution parameters
    neighborhood_type = 0 if Variables.neighborhood[fileNumber] == "moore" else 1
    boundary_condition = 0 if Variables.boundary_conditions[fileNumber] == "abs" else 1

    # Execute the kernel
    kernel = program.grain_growth
    kernel.set_args(
        structure_buf, np.uint32(size_x), np.uint32(size_y), np.uint32(size_z),
        np.uint32(neighborhood_type), np.uint32(boundary_condition)
    )
    cl.enqueue_nd_range_kernel(queue, kernel, (structure_np.size,), None)

    # Copy the result back to the host
    cl.enqueue_copy(queue, structure_np, structure_buf).wait()

    return structure_np.reshape((size_x, size_y, size_z)).tolist()
