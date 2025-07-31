import numpy
import math
from calc import *
from data import *

from geometry_calc import * 

__resolution = 2 #  resolution when calculate chain area 
__point_n = 100 # points of the routeA
__Tini = 3000 # initial temprature 
__Tmin = 20 # min tmp 
__k = 20 # internal circulation 

def print_info(): 
    print(f"解析度(两点之间采样数目): {__resolution}")
    print(f"点数目: {__point_n}")
    print(f"初始温度: {__Tini}") 
    print(f"最小温度: {__Tmin}")
    print(f"同温探索次数: {__k}")

def aim_function(points): 
    ret = get_chain_area_calc(points, __resolution)
    return ret[0] - 0.1 * ret[1]

def move_point(path, max_move_distance, bounds):
    """
    随机移动路径中的一个中间点。

    参数:
    path (np.ndarray): 当前的点链，形状为 (n, 2)。
    max_move_distance (float): 单个点在每个坐标轴上可能移动的最大距离。
    bounds (tuple): 矩形边界，格式为 ((x_min, y_min), (x_max, y_max))。

    返回:
    np.ndarray: 一个新的点链，形状为 (n, 2)。
    """
    new_path = np.copy(path)
    n = len(new_path)

    # 确保路径至少有3个点才能移动中间点
    if n <= 2:
        return new_path

    # 1. 随机选择一个要移动的点 (不包括首尾点)
    # np.random.randint(low, high) 生成 [low, high) 之间的整数
    idx_to_move = np.random.randint(1, n - 1)
    
    # 2. 生成一个在[-max_dist, +max_dist]范围内的随机移动向量
    move_vector = np.random.uniform(-max_move_distance, max_move_distance, size=2)
    
    # 3. 应用移动
    new_path[idx_to_move] += move_vector
    
    # 4. 边界检查和约束：确保移动后的点不会超出边界
    ld, rt = bounds
    # np.clip 会将数组中的值限制在一个区间内
    new_path[idx_to_move] = np.clip(new_path[idx_to_move], a_min=ld, a_max=rt)
    
    return new_path

def swap_2opt(path):
    new_path = np.copy(path)
    n = len(new_path)
    if n < 4: return new_path

    # 确保选择的两个点之间至少有一个点
    # i 从 1 到 n-3, j 从 i+1 到 n-2
    i = np.random.randint(1, n - 2)
    j = np.random.randint(i + 1, n - 1)
    
    # 提取并反转 new_path 在 [i, j+1) 区间内的部分，即包含 i 和 j
    segment_to_reverse = new_path[i:j+1]
    new_path[i:j+1] = segment_to_reverse[::-1]
    
    return new_path

def generate_neighbor(current_path, temperature, initial_temperature, bounds):
    """
    根据当前温度，随机选择一种策略来生成一个邻域解。

    参数:
    current_path (np.ndarray): 当前的点链解，形状为 (n, 2)。
    temperature (float): 当前的模拟退火温度。
    initial_temperature (float): 初始温度，用于归一化。
    bounds (tuple): 矩形边界，格式为 ((x_min, y_min), (x_max, y_max))。

    返回:
    np.ndarray: 一个新的点链解，形状为 (n, 2)。
    """
    # 归一化温度 (0到1之间)
    norm_temp = temperature / initial_temperature
    
    # 动态定义不同策略的概率
    # 高温时，swap（全局搜索）的概率更高
    # 低温时，move（局部搜索）的概率更高
    prob_swap = 0.5 * norm_temp + 0.1  # 概率从 0.6 线性递减到 0.1
    
    # 随机选择一种策略
    if np.random.rand() < prob_swap and len(current_path) > 3:
        # print("策略: 2-opt Swap") # 用于调试
        return swap_2opt(current_path)
    else:
        # print("策略: Move Point") # 用于调试
        # 定义一个合理的移动距离，例如边界框宽度的1/10
        ld, rt = bounds
        max_move_dist = (rt[0] - ld[0]) * 0.1 
        return move_point(current_path, max_move_dist, bounds)

def SA(): 

    print_info()

    x = random_points(__point_n, [x_min, y_min], [x_max, y_max]) # initial value 
    T = __Tini # temprature
    y = aim_function(x) # result
    t = 0 # time 

    while T > __Tmin: 
        for i in range(__k): 
            xNew = generate_neighbor(x, T, __Tini, ((x_min, y_min), (x_max, y_max)))
            yNew = aim_function(xNew) 
            if yNew > y: 
                x = xNew 
                y = yNew 
            else :  
                # print("xx", -(y - yNew) / T)
                p = math.exp(-(y - yNew) / T)
                r = np.random.uniform(low=0, high=1) 
                if r < p: 
                    x = xNew 
                    y = yNew 
        t += 1 
        T = __Tini / (t+1)
        print(f"iteration {t}, temprature {T}, current {y}") 
    return (x, y)


if __name__ == '__main__': 
# --- 您的环境参数 ---
# (假设 x_min, y_min, x_max, y_max 已经从 data.py 中定义)
# from data import x_min, y_min, x_max, y_max

# 为了独立运行，我们先定义一些假数据
    x_min, y_min, x_max, y_max = 0, 0, 100, 100

    __point_n = 10 
    __T = 1000 

# 生成初始随机点链
# 假设 random_points 函数返回的是 (n,2) 的 numpy 数组
    def random_points(n, ld, rt):
        x_coords = np.random.uniform(ld[0], rt[0], n)
        y_coords = np.random.uniform(ld[1], rt[1], n)
        return np.column_stack((x_coords, y_coords))

    initial_path = random_points(__point_n, (x_min, y_min), (x_max, y_max))

# --- 调用示例 ---
    print("原始路径:\n", np.round(initial_path, 2))

# 1. 测试 Single Point Move
    moved_path = move_point(initial_path, max_move_distance=10, bounds=((x_min, y_min), (x_max, y_max)))
    print("\n应用'Move Point'后的路径:\n", np.round(moved_path, 2))

# 2. 测试 2-opt Swap
    swapped_path = swap_2opt(initial_path)
    print("\n应用'2-opt Swap'后的路径:\n", np.round(swapped_path, 2))

# 3. 测试综合函数 (在模拟退火中使用的)
# 假设当前温度是500
    current_temperature = 500
    neighbor_path = generate_neighbor(initial_path, current_temperature, __T, ((x_min, y_min), (x_max, y_max)))
    print(f"\n在温度 {current_temperature} 时生成的邻域路径:\n", np.round(neighbor_path, 2))

        

