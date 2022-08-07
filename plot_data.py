import json
import numpy as np
import matplotlib.pyplot as plt

RAD_TO_DEG = 57.2957795

# Loading the data.json file
f = open('data.json')
data = json.load(f)

# Extracting the data from the data.json file
x_pos = list(map(lambda x:x[0], data))
y_pos = list(map(lambda x:x[1], data))
z_pos = list(map(lambda x:x[2], data))
roll = list(map(lambda x:x[3] * RAD_TO_DEG, data))
pitch = list(map(lambda x:x[4] * RAD_TO_DEG, data))
yaw = list(map(lambda x:x[5] * RAD_TO_DEG, data))

plt.plot(x_pos, label='x_pos')
plt.plot(y_pos, label='y_pos')
plt.plot(z_pos, label='z_pos')
plt.legend()
plt.xlabel('steps')
plt.ylabel('position, mm')
plt.title('position vs. steps')
plt.grid()
plt.show()

plt.plot(roll, label='roll')
plt.plot(pitch, label='pitch')
plt.plot(yaw, label='yaw')
plt.legend()
plt.xlabel('steps')
plt.ylabel('rpy, deg')
plt.title('rpy vs. steps')
plt.grid()
plt.show()