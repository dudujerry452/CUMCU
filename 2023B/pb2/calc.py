import numpy as np 

def get_ray_plane_intersection(plane_normal, plane_point, ray_origin, ray_direction):
    """
    计算一条射线与一个平面的交点。

    参数:
    plane_normal (np.ndarray): 平面的法向量，例如 np.array([0, 0, 1])。
    plane_point (np.ndarray): 平面上的任意一点，例如 np.array([0, 0, 0])。
    ray_origin (np.ndarray): 射线的起点，例如 np.array([1, 1, 10])。
    ray_direction (np.ndarray): 射线的方向向量（最好是单位向量）。

    返回:
    np.ndarray or None: 如果有交点，返回交点的3D坐标；否则返回 None。
    """
    # 确保所有输入都是numpy数组，以进行向量运算
    n = np.asarray(plane_normal, dtype=float)
    p0 = np.asarray(plane_point, dtype=float)
    r0 = np.asarray(ray_origin, dtype=float)
    d = np.asarray(ray_direction, dtype=float)

    # 归一化方向向量，确保是单位向量（这是一个好习惯）
    d = d / np.linalg.norm(d)
    
    # 1. 计算点积 n · d (分母)
    dot_nd = np.dot(n, d)
    
    # 检查射线是否与平面平行
    # 我们用一个很小的数 (1e-6) 来判断是否接近于0，以避免浮点数精度问题
    if abs(dot_nd) < 1e-6:
        # print("射线与平面平行，没有交点。")
        return None
        
    # 2. 计算 n · (p₀ - r₀) (分子)
    w = p0 - r0
    dot_nw = np.dot(n, w)
    
    # 3. 计算参数 t
    t = dot_nw / dot_nd
    
    # 4. 检查交点是否在射线的正方向
    if t < 0:
        # print("交点在射线的反方向，对于物理射线无效。")
        return None
        
    # 5. 计算交点坐标
    intersection_point = r0 + t * d
    
    return intersection_point
