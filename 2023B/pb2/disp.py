import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
import mpl_toolkits.mplot3d.art3d as art3d
from scipy.spatial.transform import Rotation

from data import *

from calc import * 


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

# --- 2. 创建3D图形和坐标轴 ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
# 设置中文字体，请根据您的操作系统选择

# --- 3. 绘制“水平面”和“海底坡面” ---
# a. 创建用于生成平面的网格坐标
x_plane = np.linspace(-50, 50, 10)
y_plane = np.linspace(-50, 50, 10)
X, Y = np.meshgrid(x_plane, y_plane)

# b. 定义“水平面” (z=0)
Z_horizontal = np.zeros_like(X)
ax.plot_surface(X, Y, Z_horizontal, alpha=0.1, color='c', rstride=1, cstride=1)
ax.text(0, 40, 0, "水平面", color='k', fontsize=12)

# c. 定义“海底坡面”
# 为了方便展示，我们让坡度方向沿Y轴方向
Z_seabed = -D_center + np.tan(alpha_rad) * Y
ax.plot_surface(X, Y, Z_seabed, alpha=0.3, color='orange', rstride=1, cstride=1)
ax.text(0, -40, -D_center - 15, "海底坡面", color='k', fontsize=12)


# --- 4. 绘制“测线方向”与“坡面法向在水平面上的投影” ---
# 我们在原点(0,0,0)处绘制各个向量
origin = [0, 0, 0]
origin2 = [0,0,-D_center]

sur_norm_000 = [0, -np.tan(alpha_rad), 1]
sur_norm = np.array(sur_norm_000)


# 法向量投影
v_proj_dir = np.array([0, -1, 0]) # 坡度沿Y轴正方向，所以投影指向Y轴正方向
ax.quiver(*origin, *v_proj_dir*40, color='red', arrow_length_ratio=0.1, label='坡面法向投影')

ax.quiver(*origin2, *sur_norm*20, color='yellow', arrow_length_ratio=0.1, label = "123")

v_0 = np.array([np.sin(beta_rad), -np.cos(beta_rad), 0])
ax.quiver(*origin, *v_0*50, color='blue', arrow_length_ratio=0.1, label='测线方向')

def paint_part(v_0, origin): 

    rotation_axis = v_0 

    rot_angle_rad = np.deg2rad(90-theta_deg/2)

    rotation_vector =  (rotation_axis/np.linalg.norm(rotation_axis))
    rr = Rotation.from_rotvec(rot_angle_rad * rotation_vector)

    v_2= np.array([v_0[1], v_0[0]*-1, 0])

    v_rotated = rr.apply(v_2);
    rr = Rotation.from_rotvec(np.deg2rad(90+theta_deg/2) * rotation_vector)
    v_rotated_1 = rr.apply(v_2);

     

    pointer_1 = get_ray_plane_intersection(sur_norm, np.array([X[0][0],Y[0][0],Z_seabed[0][0]]),origin,v_rotated)
    pointer_2 = get_ray_plane_intersection(sur_norm, np.array([X[0][0],Y[0][0],Z_seabed[0][0]]),origin,v_rotated_1)
    
    return [pointer_1, pointer_2]



xs = []
ys = []
zs = []

for i in range(0,100) :
    ret = paint_part(v_0, origin + v_0*i) 
    xs.append(ret[0][0])
    xs.append(ret[1][0])
    ys.append(ret[0][1])
    ys.append(ret[1][1])
    zs.append(ret[0][2])
    zs.append(ret[1][2])


ax.scatter(xs, ys, zs, 
               color='red',      # 点的颜色
               s=10,             # 点的大小 (size)
               depthshade=True,  # 根据深度有明暗变化，增加立体感
               label='海底测量点') # 图例标签


# ret1 = paint_part(v_0, origin)
ax.quiver(*origin, xs[0], ys[0], zs[0], color='green', arrow_length_ratio=0.1, label='v3')
ax.quiver(*origin, xs[1], ys[1], zs[1], color='green', arrow_length_ratio=0.1, label='v3')
# paint_part(v_0, origin + v_0)



# --- 6. 美化和显示图形 ---
ax.set_xlabel("X 轴")
ax.set_ylabel("Y 轴")
ax.set_zlabel("Z 轴 (深度)")

# 设置坐标轴范围以获得更好的视图
ax.set_xlim([-50, 50])
ax.set_ylim([-50, 50])
ax.set_zlim([-D_center-30, 20])

# 调整视角
ax.view_init(elev=25, azim=-70)
ax.set_title("问题二：几何关系示意图", fontsize=16)

plt.show()
