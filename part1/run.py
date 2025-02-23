import numpy as np
from src import *

# Create nodes
nodes = np.array ([[0,0,0], [1,0,0]])
connections = np.array ([[0,1]])
E = 210e9
v = 0.9
A = 0.01
I = 1e-5
Iz = I
Iy = I
Ip = I
J = I
material = {1:[E, v, A, Iz, Iy, Ip, J, [0,0,1]]}
domain_elements = {1:[0]}
fixed_nodes = [0]
pinned_nodes = []
load_dict = {1:[0,-1000,0,0,0,0]}

disps,rxns = generate_mesh_and_solve (nodes,connections,material, domain_elements, fixed_nodes,pinned_nodes, load_dict)