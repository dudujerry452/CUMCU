import numpy as np

drone_d = [0,100,98,112,105,98,112,105,98,112]
drone_theta = [0,0,40.1,80.21,119.75,159.86,199.96,240.07,280.17,320.28]

ds = np.array(drone_d)
thetas = np.array(np.radians(drone_theta))

drone_x = ds*np.cos(thetas)
drone_y = ds*np.sin(thetas)
