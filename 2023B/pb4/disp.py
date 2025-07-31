import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from shapely.geometry import Polygon

from data import *
from calc import *
from find_ray_surface_intersection import *
from geometry_calc import *
from algo_calc import *

# --- 字体设置 ---
try:
    font_list = ['PingFang SC', 'Microsoft YaHei', 'SimHei', 'Heiti TC', 'Arial Unicode MS']
    plt.rcParams['font.sans-serif'] = font_list
    plt.rcParams['axes.unicode_minus'] = False
    print(f"成功设置字体参数，将尝试使用列表: {font_list}")
except Exception:
    print("警告：字体参数设置失败。")

# --- 创建绘图区域 ---
fig, ax = plt.subplots(figsize=(12, 9))
X, Y = np.meshgrid(x_coords, y_coords)
levels = np.linspace(np.nanmin(z_values), np.nanmax(z_values), 21)
contour_filled = ax.contourf(X, Y, z_values, levels=levels, cmap='viridis_r', extend='both')
cbar = fig.colorbar(contour_filled, ax=ax)
cbar.set_label('海水深度 / m', rotation=270, labelpad=15)
ax.set_title('测线覆盖区域与重叠分析', fontsize=16)
ax.set_xlabel('横向坐标 / m (由西向东)')
ax.set_ylabel('纵向坐标 / m (由南向北)')
ax.set_aspect('equal', 'box')
ax.grid(True, linestyle='--', alpha=0.6)

# --- 准备测线数据 ---

def plot_points(ax, points1): 

# 第一条测线
    ax.plot([p[0] for p in points1], [p[1] for p in points1], 'b-o', label='测线1')

# --- 计算条带和多边形 ---
# 获取两条测线对应的海底边缘点链
    result = get_chain_area(points1, 9)
    poly1 = result[0]

    plot_polygon(ax, poly1, 'cyan', label=f'条带1覆盖范围')

# 高亮显示重叠区域
    intersection_poly = result[1]
    for intp in intersection_poly: 
        plot_polygon(ax, intp, 'red', alpha=0.8) 

# 在图上添加文字说明
    result_text = f"重叠率: {result[2]/(result[0].area - result[2]+1e-6):.2%}"
    ax.text(0.95, 0.95, result_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.8))

    result_text = f"覆盖率: {(result[0].area - result[2])/(total_sea_area):.2%}"
    ax.text(0.95, 0.85, result_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.8))

# init_points_1 = [[1,1], [1,2], [2,3], [2,2], [3,2]]
# init_points_1 = [np.array(i) * 1852 for i in init_points_1]
# init_points_1 = random_points(10, [x_min, y_min], [x_max, y_max])
# print(init_points_1)
pointret = SA() 
init_points_1 = pointret[0]
plot_points(ax, init_points_1)

print("\n正在强制设定坐标轴范围为原始数据框...")
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

ax.legend()
plt.tight_layout()
plt.show()
