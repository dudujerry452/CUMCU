import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# 假设这些模块包含了您需要的数据和函数
from data import x_coords, y_coords, z_values
# from calc import *
# from find_ray_surface_intersection import *
# from specific_calc import *

# --- 字体设置 ---
try:
    font_list = [
        'PingFang SC',       # 适用于 macOS
        'Microsoft YaHei',   # 适用于 Windows (微软雅黑)
        'SimHei',            # 适用于 Windows (黑体)
        'Heiti TC',          # 适用于 macOS
        'Arial Unicode MS',  # 一个通用的Unicode字体
    ]
    plt.rcParams['font.sans-serif'] = font_list
    plt.rcParams['axes.unicode_minus'] = False
    print(f"成功设置字体参数，将尝试使用列表: {font_list}")
except Exception:
    print("警告：字体参数设置失败。")

# ======================================================
# --- 1. 计算梯度 ---
# ======================================================
# np.gradient会返回每个方向的梯度分量
# 注意顺序：第一个返回值是沿axis=0 (Y方向)的梯度，第二个是沿axis=1 (X方向)的梯度
gz, gx = np.gradient(z_values, y_coords, x_coords)

# 计算梯度的模，代表坡度的陡峭程度
gradient_magnitude = np.sqrt(gx**2 + gz**2)

# ======================================================
# --- 2. 创建包含两个子图的Figure ---
# ======================================================
# plt.subplots(1, 2) 创建一个1行2列的网格，并返回figure对象和两个axes对象
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 9))

# --- 3. 在第一个子图 (ax1) 上绘制原始等高线图 ---
ax1.set_title('海底地形等高线图', fontsize=16)
X, Y = np.meshgrid(x_coords, y_coords)
levels = np.linspace(np.nanmin(z_values), np.nanmax(z_values), 21)
contour_filled = ax1.contourf(X, Y, z_values, levels=levels, cmap='viridis_r', extend='both')
contour_lines = ax1.contour(X, Y, z_values, levels=levels, colors='black', linewidths=0.5)
ax1.clabel(contour_lines, inline=True, fontsize=8, fmt='%.1f')
fig.colorbar(contour_filled, ax=ax1, label='海水深度 / m', orientation='vertical')
ax1.set_xlabel('横向坐标 / NM (由西向东)')
ax1.set_ylabel('纵向坐标 / NM (由南向北)')
ax1.set_aspect('equal', 'box')
ax1.grid(True, linestyle='--', alpha=0.6)

# --- 4. 在第二个子图 (ax2) 上绘制梯度图 ---
ax2.set_title('海底地形梯度图 (坡度与方向)', fontsize=16)

# a. 绘制梯度大小的背景颜色图
grad_contour = ax2.contourf(X, Y, gradient_magnitude, levels=20, cmap='hot')
fig.colorbar(grad_contour, ax=ax2, label='梯度大小 (坡度)', orientation='vertical')

# b. 绘制表示梯度方向的箭头 (Quiver Plot)
# 如果数据点太多，全部绘制会很乱，所以我们进行降采样
skip = 30  # 每隔5个点绘制一个箭头
ax2.quiver(X[::skip, ::skip], Y[::skip, ::skip], 
           gx[::skip, ::skip], gz[::skip, ::skip],
           color='white',
           scale=np.nanmax(gradient_magnitude)*2) # 调整scale使箭头大小合适

ax2.set_xlabel('横向坐标 / NM (由西向东)')
ax2.set_ylabel('纵向坐标 / NM (由南向北)')
ax2.set_aspect('equal', 'box')
ax2.grid(True, linestyle='--', alpha=0.6)


# --- 5. 最终调整和显示 ---
fig.suptitle('海底地形分析', fontsize=20) # 为整个Figure添加一个总标题
plt.tight_layout(rect=[0, 0, 1, 0.96]) # 调整布局，为总标题留出空间
plt.show()
