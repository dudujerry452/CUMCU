import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.optimize import root_scalar # 导入数值求解器

def find_ray_surface_intersection(ray_origin, ray_direction, interpolator_func):
    """
    使用数值方法计算射线与插值曲面的交点。

    参数:
    ray_origin (np.ndarray): 射线的起点。
    ray_direction (np.ndarray): 射线的方向向量（应为单位向量）。
    interpolator_func (callable): 您创建的插值器对象。

    返回:
    np.ndarray or None: 交点的3D坐标，或如果没有找到交点则返回None。
    """
    # 确保方向是单位向量
    d = np.asarray(ray_direction) / np.linalg.norm(ray_direction)
    r0 = np.asarray(ray_origin)

    # 1. 定义差距函数 (作为内部函数，可以访问外部的 r0, d, interpolator_func)
    def difference_function(t):
        """计算在距离t处，射线Z坐标与曲面Z坐标的差值。"""
        # 如果t是负数，则没有物理意义，返回一个大数
        if t < 0:
            return 1e9 # 返回一个大数，避免求解器找到负根
            
        # 计算射线在距离t处的位置
        point_on_ray = r0 + t * d
        px, py, pz = point_on_ray
        
        # 使用插值器计算曲面在(px, py)处的深度
        # 查询时要用(x,y)顺序，与插值器定义时一致
        z_surface = interpolator_func([px, py])
        
        # 如果点超出了插值范围，返回一个大数
        if np.isnan(z_surface):
            return 1e9
            
        # 返回垂直差距
        return pz - z_surface

    # 2. 使用数值求解器寻找根
    # 我们需要提供一个搜索范围 [t_min, t_max]
    # t_min=0，因为我们只关心前方的交点
    # t_max可以设为一个足够大的数，能覆盖整个海域即可
    try:
        # brentq 是一个非常快速和稳健的求根算法
        sol = root_scalar(f=difference_function, bracket=[0, 500], method='brentq')
        
        if sol.converged:
            # 如果成功找到根，t_intersection 就是我们要求的t值
            t_intersection = sol.root
            intersection_point = r0 + t_intersection * d
            return intersection_point
        else:
            return None
            
    except ValueError:
        # 如果 difference_function 在 bracket 两端同号，brentq会报错
        # 这通常意味着没有交点，或者有偶数个交点（例如切线）
        # print("在搜索范围内未找到交点（函数值在两端同号）。")
        return None

# --- 使用示例 ---
# a. 定义一条射线
# origin = np.array([50, 50, 0]) # 从海域中心的海面发出
# direction = np.array([0.1, 0, -1]) # 稍微偏离垂直向下

# # b. 调用函数计算交点
# intersection = find_ray_surface_intersection(origin, direction, interpolator)

