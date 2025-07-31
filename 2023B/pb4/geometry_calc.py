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



# the difference between this and get_chain_area is this don't return poly
def get_chain_area_calc(points, resolution):  
    total_overlay_area = 0.0
    # total_poly = Polygon().buffer(0)
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

    total_poly_area = Polygon(np.vstack([total_pointsA, total_pointsB[::-1]])).area
    return (total_poly_area - total_overlay_area, total_overlay_area)

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


def random_points(n, ld, rt):
    """
    在指定的矩形范围内生成n个随机分布的点。

    这个函数生成的点在矩形区域内是均匀分布的，
    意味着任何子区域内的点的数量都与其面积成正比。

    参数:
    n (int): 要生成的点的数量。
    ld (tuple or list): 矩形的左下角(Left-Down)坐标，格式为 (x_min, y_min)。
    rt (tuple or list): 矩形的右上角(Right-Top)坐标，格式为 (x_max, y_max)。

    返回:
    numpy.ndarray: 一个形状为 (n, 2) 的数组，每行代表一个点的 [x, y] 坐标。
    """
    # 1. 从输入参数中解析出坐标范围
    x_min, y_min = ld
    x_max, y_max = rt
    
    # 2. 为 x 和 y 坐标分别生成 n 个在指定范围内的随机数
    # np.random.uniform 在 [low, high) 区间内生成均匀分布的随机数
    random_x = np.random.uniform(low=x_min, high=x_max, size=n)
    random_y = np.random.uniform(low=y_min, high=y_max, size=n)
    
    # 3. 将 x 和 y 坐标组合成点
    # np.column_stack 是将一维数组作为列堆叠成二维数组的最有效方法
    points = [np.array([random_x[i], random_y[i]]) for i in range(len(random_x))]
    
    return points





