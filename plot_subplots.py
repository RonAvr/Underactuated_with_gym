import json
import numpy as np
import matplotlib.pyplot as plt

RAD_TO_DEG = 57.2957795

# Loading the data.json file and extracting the pos and time data
f = open('data.json')
data = json.load(f)
pos_data = data['pos_data']
time = data['time_data']

# Extracting the data from the data.json file
x_pos = list(map(lambda x:x[0], pos_data))
y_pos = list(map(lambda x:x[1], pos_data))
z_pos = list(map(lambda x:x[2], pos_data))
roll = list(map(lambda x:x[3] * RAD_TO_DEG, pos_data))
pitch = list(map(lambda x:x[4] * RAD_TO_DEG, pos_data))
yaw = list(map(lambda x:x[5] * RAD_TO_DEG, pos_data))
quat = list(map(lambda x:x[6] * RAD_TO_DEG, pos_data))

fig, axs = plt.subplots(3, 3)
axs[0,0].plot(x_pos)
axs[0,0].grid()
axs[0,0].set(ylabel='position, mm')
axs[0,0].set_title('x position')

axs[0,1].plot(y_pos)
axs[0,1].grid()
axs[0,1].set_title('y position')

axs[0,2].plot(z_pos)
axs[0,2].grid()
axs[0,2].set_title('z position')

axs[1,0].plot(roll)
axs[1,0].grid()
axs[1,0].set(ylabel='deg')
axs[1,0].set_title('roll')

axs[1,1].plot(pitch)
axs[1,1].grid()
axs[1,1].set_title('pitch')

axs[1,2].plot(yaw)
axs[1,2].grid()
axs[1,2].set_title('yaw')

axs[2,0].plot(quat)
axs[2,0].grid()
axs[2,0].set(ylabel='deg')
axs[2,0].set_title('quat')

plt.show()