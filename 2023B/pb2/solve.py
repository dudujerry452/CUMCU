import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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


# --- 1. 读取数据 (代码无需改动) ---
try:
    df = pd.read_excel('data.xlsx', header=None)
except FileNotFoundError:
    print("错误：请确保 'data.xlsx' 文件与此脚本在同一目录下。")
    exit()

# --- 2. 精确切分数据 (代码无需改动) ---
try:
    x_coords = df.iloc[1, 2:].dropna().to_numpy().astype(float)
    y_coords = df.iloc[2:, 1].dropna().to_numpy().astype(float)
    z_values = df.iloc[2:, 2:].dropna(how='all').to_numpy().astype(float)
except (ValueError, IndexError):
    print("数据切分或转换时出错。请确认Excel文件结构。")
    exit()

# --- 3. 诊断与维度修正 (代码无需改动) ---
z_rows, z_cols = z_values.shape
y_coords = y_coords[:z_rows]
x_coords = x_coords[:z_cols]
if z_values.shape != (len(y_coords), len(x_coords)):
    print(f"致命错误：维度不匹配！无法绘图。")
    exit()

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
plt.tight_layout()
plt.show()
