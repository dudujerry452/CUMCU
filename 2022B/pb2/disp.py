import matplotlib.pyplot as plt
import numpy as np

from data import drone_x 
from data import drone_y

import calc

x = drone_x
y = drone_y

fig, ax = plt.subplots()

plt.scatter(x,y,color='red',s=50,marker='o')

solveret = calc.solve(0,9,1,3)

pt1 = solveret[0]
circle = plt.Circle((pt1[0], pt1[1]), pt1[2], color='blue', fill=False, linestyle='--', linewidth=2)
ax.add_patch(circle)

pt2 = solveret[1]
circle = plt.Circle((pt2[0], pt2[1]), pt2[2], color='blue', fill=False, linestyle='--', linewidth=2)
ax.add_patch(circle)

pt3 = solveret[2]
circle = plt.Circle((pt3[0], pt3[1]), pt3[2], color='blue', fill=False, linestyle='--', linewidth=2)
ax.add_patch(circle)

maincircle = plt.Circle((0,0),100, color='yellow', fill=False, linestyle='--', linewidth=2)
ax.add_patch(maincircle)






ax.axhline(y=0, color='black', linewidth=1.2)
ax.axvline(x=0, color='black', linewidth=1.2)
# -----------------------------------------

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("drones")

ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()
ax.set_aspect('equal', adjustable='box')

plt.show()
