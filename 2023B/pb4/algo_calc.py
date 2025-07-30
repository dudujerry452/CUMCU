import numpy
from calc import *
from data import *

from geometry_calc import * 

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





