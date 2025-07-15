import matplotlib.pyplot as plt
import numpy as np

from data import x_coords_numpy as x
from data import y_coords_numpy as y

fig, ax = plt.subplots()
plt.scatter(x,y,color='red',s=10,marker='o')

ax.axhline(y=0, color='black', linewidth=1.2)
ax.axvline(x=0, color='black', linewidth=1.2)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("panels")

ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()
ax.set_aspect('equal', adjustable='box')

plt.show()

