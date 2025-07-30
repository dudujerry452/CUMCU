import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon

import math

from data import *
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


def get_chain_area(points, resolution): 
    total_overlay_area = 0.0
    # total_poly = Polygon().buffer(0)
    intersection_poly = []
    total_pointsA = []
    total_pointsB = []
    for i in range(len(points)-1): 
        progress = 0.0
        pointsA = []
        pointsB = []
        for j in range(0, resolution+2): 
            ret = gethitpoint1(points[i], points[i+1], progress)
            pointsA.append(ret[0])
            pointsB.append(ret[1])
            progress += 1/(resolution+1)
        total_poly = Polygon().buffer(0)
        if len(total_pointsA) != 0: 
            total_poly = Polygon(np.vstack([total_pointsA, total_pointsB[::-1]])).buffer(0)
        total_pointsA.extend(pointsA) 
        total_pointsB.extend(pointsB)
        pointsB = pointsB[::-1]
        pointsA = np.vstack([pointsA, pointsB])

        poly = Polygon(pointsA).buffer(0)

        interpoly = total_poly.intersection(poly)
        total_overlay_area += interpoly.area
        # intersection_poly = intersection_poly.union(interpoly)
        intersection_poly.append(interpoly)

    total_poly = Polygon(np.vstack([total_pointsA, total_pointsB[::-1]]))
    return (total_poly, intersection_poly, total_overlay_area)

def plot_polygon(ax, poly, facecolor, edgecolor='black', alpha=0.5, label=None):
    """
    一个更健壮的函数，可以绘制单个Polygon或MultiPolygon。
    """
    if poly is None or poly.is_empty:
        return

    # 判断传入的几何体类型
    if isinstance(poly, MultiPolygon):
        # 如果是MultiPolygon，就遍历其中的每一个Polygon并分别绘制
        # 只为第一个多边形添加标签，避免图例重复
        first = True
        for p in poly.geoms:
            x, y = p.exterior.xy
            if first:
                ax.fill(x, y, alpha=alpha, fc=facecolor, ec=edgecolor, label=label)
                first = False
            else:
                ax.fill(x, y, alpha=alpha, fc=facecolor, ec=edgecolor)
    elif isinstance(poly, Polygon):
        # 如果是单个Polygon，按原方式绘制
        x, y = poly.exterior.xy
        ax.fill(x, y, alpha=alpha, fc=facecolor, ec=edgecolor, label=label)
