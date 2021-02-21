from __future__ import division

import argparse
import numpy as np
import precice
from matplotlib import pyplot as plt

configuration_file_name = "../precice-config.xml"
participant_name = "Fluid"
mesh_name = "Fluid-Mesh"
write_data_name = 'Force'
read_data_name = 'Displacement'

num_vertices = 100  # Number of vertices

solver_process_index = 0
solver_process_size = 1

interface = precice.Interface(participant_name, configuration_file_name,
                              solver_process_index, solver_process_size)

mesh_id = interface.get_mesh_id(mesh_name)
dimensions = interface.get_dimensions()

vertices = np.zeros((num_vertices, dimensions))
write_data = np.zeros((num_vertices, dimensions))

W = .1
H = 1
x_left = 0 - W/2
y_bottom = 0
y_top = y_bottom + H
F_max = 1

vertices[:, 0] = x_left  # all vertices are at left side of beam
vertices[:, 1] = np.linspace(y_bottom, y_top, num_vertices)  # have num_vertices equally disrtibuted vertices

write_data[:, 0] = F_max * vertices[:, 1] / H  # linearly increasing load
write_data[:, 1] = 0

vertex_ids = interface.set_mesh_vertices(mesh_id, vertices)
read_data_id = interface.get_data_id(read_data_name, mesh_id)
write_data_id = interface.get_data_id(write_data_name, mesh_id)

dt = interface.initialize()
t = 0

time = []
u_tip = []
v_tip = []
time.append(0.0)
u_tip.append(0.0)
v_tip.append(0.0)

while interface.is_coupling_ongoing():
    if interface.is_action_required(
            precice.action_write_iteration_checkpoint()):
        interface.mark_action_fulfilled(
            precice.action_write_iteration_checkpoint())

    if interface.is_read_data_available():  # we don't care about data that is read, but will do it anyway.
        read_data = interface.read_block_vector_data(read_data_id, vertex_ids)

    write_data[:, 0] = F_max * vertices[:, 1] / H  # linearly increasing load
    write_data[:, 1] = 0

    if interface.is_write_data_required(dt):
        interface.write_block_vector_data(
            write_data_id, vertex_ids, write_data)

    print("DUMMY: Advancing in time")
    recv_dt = interface.advance(dt)
    assert(recv_dt == dt)

    if interface.is_action_required(
            precice.action_read_iteration_checkpoint()):
        print("DUMMY: Reading iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_read_iteration_checkpoint())

    if interface.is_time_window_complete():
        t += dt
        u = read_data[-1, :]
        print(read_data.shape)
        print(u)

        scale=10
        u_tip.append(u[0])
        v_tip.append(u[1]*scale)
        time.append(t)

# Plot tip displacement evolution
plt.figure()
plt.title("Fluid")
plt.plot(time, u_tip)
plt.plot(time, v_tip)
plt.xlabel("Time")
plt.ylabel("Tip displacement")
plt.legend(["x", "y * {}".format(scale)])
plt.show()

interface.finalize()
print("DUMMY: Closing fake fluid.")
