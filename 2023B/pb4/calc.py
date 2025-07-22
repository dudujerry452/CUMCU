import numpy as np 
# from data import * 
from scipy.spatial.transform import Rotation

def rotate_vector(u, v, rad):  # u : to be apply ; v : rotation vectpr; rad: angle in rad 
    v = (v/np.linalg.norm(v))
    r = Rotation.from_rotvec(rad * v) 
    return r.apply(u)

def plumb_and_rotate(u, rad):
    vertical = np.array([u[1], -u[0], 0])

    return rotate_vector(vertical, np.array([u[0],u[1],0]), rad)/np.linalg.norm(vertical)
    
def angle_between_vectors(u, v): 
    return np.arccos(np.clip(np.dot(u,v)/(np.linalg.norm(u)*np.linalg.norm(v)), -1.0, 1.0))

