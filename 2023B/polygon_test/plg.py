import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.plotting import plot_polygon

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
# --- 1. 创建两个相互重叠的正方形 ---

# pots = [[(0, 0), (0, 2), (2, 2), (2, 0)], 
#        [(1, 1), (1, 3), (3, 3), (3, 1)] ]
pots = [
     [(0,0),(0,4),(1,4),(1,0)], 
    [(0,3),(0,4),(4,4),(4,3)],
    [(0,0),(0,1),(4,1),(4,0)],
     [(3,0),(3,4),(4,4),(4,0)], 
        ]
polys = [Polygon(x) for x in pots]

# poly1的面积是 2 * 2 = 4
# poly2的面积是 2 * 2 = 4
# 它们在 (1,1) 到 (2,2) 之间有一个 1 * 1 = 1 的重叠区域

# --- 2. 用这两个重叠的多边形，创建一个MultiPolygon ---
# 这是一个有点“不规范”的MultiPolygon，因为它内部有重叠
overlapping_multipoly = MultiPolygon(polys)

# --- 3. 计算面积 ---
# a. 计算两个独立多边形的面积之和 (错误的方法)
sum_of_areas = 0
for i in polys: 
    sum_of_areas += i.area

# b. 计算这个 MultiPolygon 的 .area 属性 (正确的方法)
multipoly_area = overlapping_multipoly.area

# c. 为了验证，我们手动计算它们的并集，并计算并集的面积

union_poly = Polygon()
for i in polys: 
    union_poly = union_poly.union(i)
union_area = union_poly.area


# --- 4. 打印结果 ---
for i in range(len(polys)): 
    print(f"多边形{i}的面积: {polys[i].area}")
print(f"两个面积的简单算术和 (错误的总面积): {sum_of_areas}")
print("---")
print(f"【关键】MultiPolygon的.area属性计算出的面积: {multipoly_area}")
print(f"手动计算Union后的面积: {union_area}")
print("---")
print(f"预期面积应该是 (4 + 4 - 1) = 7.0。计算结果与预期相符。")

# --- 5. 可视化 ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_title("重叠的MultiPolygon的可视化")

def plot_pots(pots, ax) : 
    for p in pots: 
        ax.text(p[0], p[1], f"{p[0]}, {p[1]}")

for i in pots: 
    plot_pots(i, ax)
    

# 绘制这个MultiPolygon，Shapely的绘图函数会自动处理重叠
plot_polygon(overlapping_multipoly, ax=ax, add_points=False, color='cyan', alpha=0.8)
ax.set_aspect('equal', 'box')
plt.show()
