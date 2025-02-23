import numpy as np
from typing import List,Dict
import math_utils as mut

class structure:
    def __init__ (self, nodes, connections):
        self.nodes = np.array (nodes)
        self.connections = np.array (connections)

class boundaryconditions:
    def __init__ (self):
        self.loads = {}
        self.supports = {}
    
    def add_load (self, node_id, Fx, Fy, Fz, Mx, My, Mz):
        self.loads[node_id] =  (Fx, Fy, Fz, Mx, My, Mz)
    
    def add_support (self, node_id, ux, uy, uz, thetax, thetay, thetaz):
        self.supports[node_id] = (ux,uy,uz,thetax,thetay,thetaz)
    
    def add_fixed_support (self, node_id):
        self.supports[node_id] = (0,0,0,0,0,0)
    
    def add_pinned_support (self, node_id):
        self.supports[node.id] = (0,0,0, None, None, None)

class materials:
    def __init__(self):
        self.mat = ()
        self.domain = ()

    def add_material(self, domain_id, E, v, A, Iz, Iy, Ip, J, z):
        self.mat[domain_id] = {'E': E,'v':v, 'A': A, 'Iz': Iz, 'Iy': Iy, 'Ip': Ip, 'J': J, 'z': z }

    def assign_domain (self, domain_id, connection_ids):
        if domain_id not in self.mat:
            raise ValueError (f"Domain {domain_id} does not exist")
        self.domains[domain_id] = connection_ids

def assemble_global_stiffness_matrix(mesh, material_params):
    """
    Assemble the global stiffness matrix.
    """
    n_nodes = len(mesh.nodes)
    n_dofs = n_nodes * 6  # 6 DOFs per node
    K_global = np.zeros((n_dofs, n_dofs))

    for element_id, (node1, node2) in enumerate(mesh.connections):
        # Get material properties
        domain_id = next((k for k, v in material.domains.items() if element_id in v), None)
        if domain_id is None:
            raise ValueError(f"Element {element_id} is not assigned to any domain.")
        props = material_params.mat[domain_id]

        # Compute local stiffness matrix
        L = np.linalg.norm(mesh.nodes[node2] - mesh.nodes[node1])
        k_local = mut.local_elastic_stiffness_matrix_3D_beam(props['E'],props['v'],props['A'],L,props['Iy'],props['Iz'],props['J'])

        # Compute transformation matrix
        node1_loc=mesh.nodes[node1]
        node2_loc=mesh.nodes[node2]
        gamma = mut.rotation_matrix_3D(node1_loc[0],node1_loc[1],node1_loc[2],node2_loc[0],node2_loc[1],node2_loc[2],props['z'])
        T = mut.transformation_matrix_3D(gamma)

        # Transform to global coordinates
        k_global = T.T @ k_local @ T

        # Assemble into global stiffness matrix
        dofs = np.array([node1*6, node1*6+1, node1*6+2, node1*6+3, node1*6+4, node1*6+5,
                         node2*6, node2*6+1, node2*6+2, node2*6+3, node2*6+4, node2*6+5])
        for i in range(12):
            for j in range(12):
                K_global[dofs[i], dofs[j]] += k_global[i, j]

    return K_global


def solve_system(K_global, boundary_conditions):
    """
    Solve the system for unknown displacements and reaction forces.

    Parameters:
        K_global (np.ndarray): Global stiffness matrix of shape (n_dofs, n_dofs).
        boundary_conditions (BoundaryConditions): Object containing boundary conditions and applied loads.

    Returns:
        displacements (np.ndarray): Array of displacements for all DOFs.
        reactions (np.ndarray): Array of reaction forces for all DOFs.
    """
    n_dofs = K_global.shape[0]  # Total number of DOFs
    displacements = np.zeros(n_dofs)  # Initialize displacements
    reactions = np.zeros(n_dofs)  # Initialize reactions

    # Identify known and unknown DOFs
    known_dofs = []  # DOFs with known displacements (boundary conditions)
    unknown_dofs = []  # DOFs with unknown displacements

    for node_id, (ux, uy, uz, thetax, thetay, thetaz) in boundary_conditions.supports.items():
        # Map node ID to DOFs
        dofs = [node_id * 6 + i for i in range(6)]  # 6 DOFs per node
        # Check which DOFs are constrained
        if ux is not None:
            known_dofs.append(dofs[0])
            displacements[dofs[0]] = ux
        if uy is not None:
            known_dofs.append(dofs[1])
            displacements[dofs[1]] = uy
        if uz is not None:
            known_dofs.append(dofs[2])
            displacements[dofs[2]] = uz
        if thetax is not None:
            known_dofs.append(dofs[3])
            displacements[dofs[3]] = thetax
        if thetay is not None:
            known_dofs.append(dofs[4])
            displacements[dofs[4]] = thetay
        if thetaz is not None:
            known_dofs.append(dofs[5])
            displacements[dofs[5]] = thetaz

    # Unknown DOFs are all DOFs not in known_dofs
    unknown_dofs = [i for i in range(n_dofs) if i not in known_dofs]

    # Partition the global stiffness matrix
    # K_uu = K_global[np.ix_(unknown_dofs, unknown_dofs)]  # Stiffness for unknown displacements
    # K_uk = K_global[np.ix_(unknown_dofs, known_dofs)]  # Coupling stiffness
    # K_ku = K_global[np.ix_(known_dofs, unknown_dofs)]  # Coupling stiffness (transpose of K_uk)
    # K_kk = K_global[np.ix_(known_dofs, known_dofs)]  # Stiffness for known displacements

    K_uu = K_global[np.ix_(known_dofs, known_dofs)]  # Stiffness for unknown displacements
    # K_uk = K_global[np.ix_(known_dofs, unknown_dofs)]  # Coupling stiffness
    K_ku = K_global[np.ix_(unknown_dofs, known_dofs)]  # Coupling stiffness (transpose of K_uk)
    # K_kk = K_global[np.ix_(unknown_dofs, unknown_dofs)]  # Stiffness for known displacements

    # Assemble the force vector
    F = np.zeros(n_dofs)
    for node_id, (Fx, Fy, Fz, Mx, My, Mz) in boundary_conditions.loads.items():
        dofs = [node_id * 6 + i for i in range(6)]  # 6 DOFs per node
        F[dofs[0]] = Fx
        F[dofs[1]] = Fy
        F[dofs[2]] = Fz
        F[dofs[3]] = Mx
        F[dofs[4]] = My
        F[dofs[5]] = Mz

    # Partition the force vector
    F_u = F[unknown_dofs]  # Forces corresponding to unknown displacements
    F_k = F[known_dofs]  # Forces corresponding to known displacements

    # Solve for unknown displacements
    displacements[unknown_dofs] = np.linalg.solve(K_uu, F_u) #  - K_uk @ displacements[known_dofs]

    # Compute reaction forces
    reactions[known_dofs] = K_ku @ displacements[unknown_dofs] - F_k #  + K_kk @ displacements[known_dofs]

    n_nodes = int(n_dofs/6)
    displacements = displacements.reshape(n_nodes,6)
    reactions = reactions.reshape(n_nodes,6)

    return displacements, reactions


def generate_mesh_and_solve(nodes:np.ndarray, connections:np.ndarray, materialproperty:Dict, domain_elements:Dict, list_fixed_nodes_id:List, list_pinned_nodes_id:List, load_dict:Dict,) ->np.ndarray:
    """
    Given nodes, element connectivities, material properties, subdomains, boundary conditions, and external forces,
    generate mesh and solve for the system.

    INPUTS:
    nodes: a n by 3 array containing the 3D coordinates of the mesh, where n is the number of nodes.
    elements: a m by 2 array containing the connectivities of the mesh, where m is the number of elements.
    subdomain_dict: a dictionary containing the properties of the material, where the key stores the ID for the subdomain, and the value a list of properties.
            e.g., subdomain 1 with list of properties E, nu, A, I_z, I_y, I_p, J, local_z_axis
                    {1:[E,nu,A,I_z,I_y,I_p,J,local_z_axis]}
    subdomain_elements: a dictionary containing the elements subdomain assignments.
            e.g., subdomain 1 has elements 0,1 {1:[0,1]}
    list_fixed_nodes_id: a list containing the node IDs for fixed nodes.
            e.g., [0]
    list_pinned_nodes_id: a list containing the node IDs for pinned nodes.
    load_dict: a dictionary where the key is the node ID of the load applied, and the value the list representing the load applied.
            e.g., {node_id:[F_x,F_y,F_z,M_x,M_y,M_z]}

    OUTPUTS:
    disps: n by 6 array containing the global nodal displacements [u_x,u_y,u_z,theta_x,theta_y,theta_z]
    rxns: n by 6 array containing the global rxn forces
    """

    mesh = structure(nodes,connections)
    mat=materials()
    for item in materialproperty.items():
        node_id,mat_params=item
        mat.add_material (domain_id=node_id,E=mat_params[0], v=mat_params[1], A=mat_params[2], Iz=mat_params[3], Iy=mat_params[4], Ip=mat_params[5], J=mat_params[6], z=mat_params[7])

    for item in domain_elements.items():
        sub_id,elements_in_sub = item
        mat.assign_domain(sub_id,elements_in_sub)

    bcs=boundaryconditions()
    for fixed_id in list_fixed_nodes_id:
        bcs.add_fixed_support(fixed_id)

    for pinned_id in list_pinned_nodes_id:
        bcs.add_pinned_support(pinned_id)

    for item in load_dict.items():
        node_id,load = item
        bcs.add_load(node_id, Fx=load[0], Fy=load[1], Fz=load[2], Mx=load[3], My=load[4], Mz=load[5])

    K_global=assemble_global_stiffness_matrix(mesh,mat)

    disps,rxns=solve_system(K_global,bcs)

    return disps,rxns