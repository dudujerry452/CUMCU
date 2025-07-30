import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import math

from data import x_coords, y_coords, z_values, interpolator, theta_rad
from calc import *
from find_ray_surface_intersection import *
from specific_calc import *

# --- 字体设置 (最终解决方案) ---
# 提供一个包含多种常见中文字体的列表
# Matplotlib会依次尝试，直到找到一个可用的
try:
    font_list = [
        'PingFang SC',       # 适用于 macOS
        'Microsoft YaHei',   # 适用于 Windows (微软雅黑)
        'SimHei',            # 适用于 Windows (黑体)
        'Heiti TC',          # 适用于 macOS
        'Arial Unicode MS',  # 一个通用的Unicode字体
    ]
    plt.rcParams['font.sans-serif'] = font_list
    plt.rcParams['axes.unicode_minus'] = False # 正常显示负号
    print(f"成功设置字体参数，将尝试使用列表: {font_list}")
except Exception:
    print("警告：字体参数设置失败。")

# --- 4. 绘图 (代码无需改动) ---
fig, ax = plt.subplots(figsize=(12, 9))
X, Y = np.meshgrid(x_coords, y_coords)
levels = np.linspace(np.nanmin(z_values), np.nanmax(z_values), 21)
contour_filled = ax.contourf(X, Y, z_values, levels=levels, cmap='viridis_r', extend='both')
contour_lines = ax.contour(X, Y, z_values, levels=levels, colors='black', linewidths=0.5)
ax.clabel(contour_lines, inline=True, fontsize=8, fmt='%.1f')
cbar = fig.colorbar(contour_filled, ax=ax)
cbar.set_label('海水深度 / m', rotation=270, labelpad=15)
ax.set_title('海底地形等高线图', fontsize=16)
ax.set_xlabel('横向坐标 / NM (由西向东)')
ax.set_ylabel('纵向坐标 / NM (由南向北)')
ax.set_aspect('equal', adjustable='box')
ax.grid(True, linestyle='--', alpha=0.6)


init_points = [[1,1], [1,2], [2,3], [2,2], [3,2]]
points = []
points_listx = []
points_listy = []
for i in init_points: 
    points.append(np.array(i)*1852)
    points_listx.append(points[len(points)-1][0])
    points_listy.append(points[len(points)-1][1])

# for i in range(len(points)-1): 
#     ax.plot(points[i][0], points[i+1][0],
#             points[i][1], points[i+1][1], 
#             linewidth = 20,
#             color='blue', 
#             linestyle='--')
    # ax.plot(points[i][0], points[i][1], 
    #         linewidth = 2,
    #         color='blue', 
    #         linestyle='--')
ax.plot(points_listx, points_listy, 
            linewidth = 2,
            color='blue', 
            linestyle='--')

hitpoints = getchainpoints(points, 2)

print("hitpoints", hitpoints[0])

for i,j,_ in hitpoints[0]: 
    ax.scatter(i, j, color='blue', s=50, marker='o')
for i,j,_ in hitpoints[1]: 
    ax.scatter(i, j, color='red', s=50, marker='o')

# ax.scatter(point1[0], point1[1], color='blue', s=50, marker='o')
# ax.scatter(point2[0], point2[1], color='blue', s=50, marker='o')
# ax.scatter(hitpoint[0][0], hitpoint[0][1], color='blue', s=50, marker='o')
# ax.scatter(hitpoint[1][0], hitpoint[1][1], color='blue', s=50, marker='o')






plt.tight_layout()
plt.show()
