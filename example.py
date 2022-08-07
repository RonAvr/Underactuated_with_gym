import gym
import numpy as np
import matplotlib.pyplot as plt

# Making the new environment
env = gym.make("Example")

# Resetting the environment
observation, infos = env.reset(seed=42, return_info=True)

# Resetting the position of the relevant joints
# qpos_reset = np.array([ 0, 0.25, 0, 0, 0.25, 0, 0, -0.2, 0])
qpos_reset = np.array([ 0, 0.25, 0, 0, 0.25, 0, 0, -0.2, 0, 0, 0, 0, 0, 0, 0, 0])
env.set_reset(qpos_reset)

# Number of loops the simulation going to loop through
root_loop = 1000
loop = 8 * root_loop

# array to store all the position data
pos_data = []

for i in range(loop):

    if (i%root_loop == 0):
        # Evaluating the value of the activation of the motors
        c = i/root_loop
        ctrl = 0.00001
        k_r = 1 #coefficient for the right motor
        k_l = 1 #coefficient for the left motor
        k_c = 3 #coefficient for the center motor

        # activating 3 of the motors in certain value
        env.set_motor_ctrl([k_r * c * ctrl, k_l *  c * ctrl, k_c *  c * ctrl])

    # Getting target body pos
    target_body_pos = env.get_body_pos('target_body')
    pos_data.append(target_body_pos)

    # Taking a step and rendering the environment
    env.sim.step()

# Extracting all the data
x_pos = list(map(lambda x:x[0], pos_data))
y_pos = list(map(lambda x:x[1], pos_data))
z_pos = list(map(lambda x:x[2], pos_data))
roll = list(map(lambda x:x[3], pos_data))
pitch = list(map(lambda x:x[4], pos_data))
yaw = list(map(lambda x:x[5], pos_data))

plt.plot(yaw)
plt.show()