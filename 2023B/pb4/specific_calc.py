import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import math

from data import x_coords, y_coords, z_values, interpolator, theta_rad
from calc import *
from find_ray_surface_intersection import *

def gethitpoint1(point1, point2, pos):
    if pos < 1e-6: 
        pos = 1e-6

    vec_origin = point2 - point1 
    vec = vec_origin * pos
    origin = point1 + vec

    vec1 = plumb_and_rotate(vec, -(math.pi - theta_rad)/2)
    vec2 = plumb_and_rotate(vec, -(math.pi + theta_rad)/2)
    
    hitpoint = []
    hitpoint.append(find_ray_surface_intersection(np.array([origin[0],origin[1],0]), vec1, interpolator))

    hitpoint.append(find_ray_surface_intersection(np.array([origin[0],origin[1],0]), vec2, interpolator))
    return hitpoint
def getwidth(point1, point2, pos):

    hitpoint = gethitpoint1(point1, point2, pos)

    hit0 = np.array([hitpoint[0][0], hitpoint[0][1]])
    hit1 = np.array([hitpoint[1][0], hitpoint[1][1]])

    tsum = 0
    for p1, p2 in zip(hit0, hit1): 
        tsum += (p2-p1)**2 
    return np.sqrt(tsum)

def getchainpoints(points, resolution): 
    pointsA = []
    pointsB = []
    for i in range(len(points)-1): 
        progress = 0.0
        for j in range(0, resolution+2): 
            ret = gethitpoint1(points[i], points[i+1], progress)
            pointsA.append(ret[0])
            pointsB.append(ret[1])
            progress += 1/(resolution+1)
    return [pointsA, pointsB]
