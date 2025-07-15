import pandas as pd

# 这是您在拥有真实文件时需要执行的核心代码
file_path = 'pos.xlsx'
df = pd.read_excel(file_path)

# 将两列数据分别提取到 pandas Series 中 (其行为与 NumPy 数组非常相似)
x_coords_series = df['x坐标 (m)']
y_coords_series = df['y坐标 (m)']

# 转换为 NumPy 数组
x_coords_numpy = x_coords_series.to_numpy()
y_coords_numpy = y_coords_series.to_numpy()

