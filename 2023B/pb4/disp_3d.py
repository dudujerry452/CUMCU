import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # 导入3D绘图工具包
import math

# 假设这些模块包含了您需要的数据和函数
from data import x_coords, y_coords, z_values, interpolator, theta_rad
from calc import *
from find_ray_surface_intersection import *


# --- 字体设置 ---
try:
    font_list = ['PingFang SC', 'Microsoft YaHei', 'SimHei', 'Heiti TC', 'Arial Unicode MS']
    plt.rcParams['font.sans-serif'] = font_list
    plt.rcParams['axes.unicode_minus'] = False
    print(f"成功设置字体参数，将尝试使用列表: {font_list}")
except Exception:
    print("警告：字体参数设置失败。")

# --- 核心计算 (这部分保持不变) ---
point1_2d = np.array([1, 2]) * 1852
point2_2d = np.array([3, 4]) * 1852

vec_origin_2d = point2_2d - point1_2d 
vec_2d = vec_origin_2d / 2
origin_2d = point1_2d + vec_2d

# vec1 和 vec2 是单位方向向量

# vec1 = np.array([vec_2d[1],-vec_2d[0], 0]) / np.linalg.norm(vec_2d)
vec1 = plumb_and_rotate(vec_2d, -(math.pi - theta_rad)/2)
vec2 = plumb_and_rotate(vec_2d, -(math.pi + theta_rad)/2)



# 计算交点时，起点在海平面(Z=0)
origin_3d = np.array([origin_2d[0], origin_2d[1], 0])
hitpoint1 = find_ray_surface_intersection(origin_3d, vec1, interpolator)
hitpoint2 = find_ray_surface_intersection(origin_3d, vec2, interpolator)


# ======================================================
# --- 3D 可视化部分 ---
# ======================================================

# 1. 创建一个3D图形和坐标轴
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# 2. 绘制海底地形曲面
X, Y = np.meshgrid(x_coords, y_coords)
ax.plot_surface(X, Y, z_values, cmap='viridis_r', alpha=0.6, rstride=5, cstride=5)

# 3. 在3D空间中绘制点、线和向量
# a. 海平面上的点和测线
ax.scatter(origin_3d[0], origin_3d[1], origin_3d[2], color='red', s=100, marker='X', label='声呐发射点 (海面)')
ax.plot([point1_2d[0], point2_2d[0]], [point1_2d[1], point2_2d[1]], [0, 0], 'b--', label='测线段')

# b. 可视化声呐扇面边缘的方向向量 vec1 和 vec2
# 为了让箭头可见，我们需要给它一个合适的长度
arrow_length = 500  # 假设箭头在图上显示为1000米的长度

# 使用 ax.quiver 绘制箭头
ax.quiver(origin_3d[0], origin_3d[1], origin_3d[2],
          vec1[0] * arrow_length, vec1[1] * arrow_length, vec1[2] * arrow_length,
          color='darkorange', label='边缘声束方向 vec1', arrow_length_ratio=0.1, lw=2)

ax.quiver(origin_3d[0], origin_3d[1], origin_3d[2],
          vec2[0] * arrow_length, vec2[1] * arrow_length, vec2[2] * arrow_length,
          color='cyan', label='边缘声束方向 vec2', arrow_length_ratio=0.1, lw=2)

# c. 绘制海底的撞击点和声波射线
if hitpoint1 is not None:
    ax.scatter(hitpoint1[0], hitpoint1[1], hitpoint1[2], color='darkorange', s=120, marker='*', label='撞击点1')
    ax.plot([origin_3d[0], hitpoint1[0]], [origin_3d[1], hitpoint1[1]], [origin_3d[2], hitpoint1[2]], 
            '--', color='darkorange', lw=2, label='声波射线1')

if hitpoint2 is not None:
    ax.scatter(hitpoint2[0], hitpoint2[1], hitpoint2[2], color='cyan', s=120, marker='*', label='撞击点2')
    ax.plot([origin_3d[0], hitpoint2[0]], [origin_3d[1], hitpoint2[1]], [origin_3d[2], hitpoint2[2]], 
            '--', color='cyan', lw=2, label='声波射线2')

# 4. 设置坐标轴和标题
ax.set_title('海底地形与声呐扇面3D可视化', fontsize=16)
ax.set_xlabel('横向坐标 / m (由西向东)')
ax.set_ylabel('纵向坐标 / m (由南向北)')
ax.set_zlabel('海水深度 / m')

# 确保坐标轴比例大致正确
# ax.set_aspect('equal') # 3D中设置比例比较复杂，通常自动调整即可

ax.view_init(elev=25, azim=-110)
ax.legend()

plt.show()
