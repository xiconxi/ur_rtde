import numpy as np 
import trimesh
from trimesh.permutate import transform

def oriented_axis(X: np.ndarray):
    X -= np.mean(X, axis=0)
    w, V = np.linalg.eig(np.dot( X.transpose(), X))
    return -V/np.min(w)

if __name__ == '__main__':
    mesh  = trimesh.load_mesh("./data/tms_coil.obj")
    mesh.vertices -= np.mean(mesh.vertices, axis=0)
    transform = oriented_axis(mesh.vertices)
    print(np.linalg.det(transform))
    mesh.vertices = np.dot(mesh.vertices, transform[:3, :3] ) 
    mesh.export("./data/tms_coil_oriented.obj")