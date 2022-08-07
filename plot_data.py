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

plt.plot(time, x_pos, label='x_pos')
plt.plot(time, y_pos, label='y_pos')
plt.plot(time, z_pos, label='z_pos')
plt.legend()
plt.xlabel('time, sec')
plt.ylabel('position, mm')
plt.title('position vs. steps')
plt.grid()
plt.show()

plt.plot(time, roll, label='roll')
plt.plot(time, pitch, label='pitch')
plt.plot(time, yaw, label='yaw')
plt.legend()
plt.xlabel('time, sec')
plt.ylabel('rpy, deg')
plt.title('rpy vs. steps')
plt.grid()
plt.show()