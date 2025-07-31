import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator



# --- 1. 读取数据 (代码无需改动) ---
try:
    ___df = pd.read_excel('data.xlsx', header=None)
except FileNotFoundError:
    print("错误：请确保 'data.xlsx' 文件与此脚本在同一目录下。")
    exit()

# --- 2. 精确切分数据 (代码无需改动) ---
try:
    x_coords = ___df.iloc[1, 2:].dropna().to_numpy().astype(float)
    y_coords = ___df.iloc[2:, 1].dropna().to_numpy().astype(float)
    z_values = ___df.iloc[2:, 2:].dropna(how='all').to_numpy().astype(float)
except (ValueError, IndexError):
    print("数据切分或转换时出错。请确认Excel文件结构。")
    exit()

# --- 3. 诊断与维度修正 (代码无需改动) ---
___z_rows, ___z_cols = z_values.shape
y_coords = y_coords[:___z_rows]
x_coords = x_coords[:___z_cols]
if z_values.shape != (len(y_coords), len(x_coords)):
    print(f"致命错误：维度不匹配！无法绘图。")
    exit()

x_coords = x_coords * 1852 
y_coords = y_coords * 1852

x_max, y_max = x_coords[-1], y_coords[-1] 
x_min, y_min = x_coords[0], y_coords[0]
total_sea_area = (x_max - x_min) * (y_max - y_min)

interpolator = RegularGridInterpolator(
    (x_coords, y_coords),  # 坐标点 (1)
    z_values.T,            # 坐标点上的值 (2)
    method='linear',
    bounds_error=False,
    fill_value=np.nan
)

# x_coords, y_coords, z_values


theta_deg = 120
theta_rad = np.deg2rad(theta_deg)


if __name__ == '__main__': 
    print("x: ")
    print(x_coords)
    print("y: ")
    print(y_coords) 
    print("z: ")
    print(z_values)

