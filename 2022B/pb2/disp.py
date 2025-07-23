import matplotlib.pyplot as plt
import numpy as np

from data import drone_x 
from data import drone_y

import calc

x = drone_x
y = drone_y

fig, ax = plt.subplots()

plt.scatter(x,y,color='red',s=50,marker='o')

solveret = calc.solve(0,4,7,9,True)
solx = [solveret[0]]
soly = [solveret[1]]
plt.scatter(solx,soly,color='blue',s=50,marker='o')


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
