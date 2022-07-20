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

for i in range(loop):
    i += 1

    if (i%root_loop == 0):
        # Evaluating the value of the activation of the motors
        c = i/root_loop
        ctrl = 0.00001
        k_r = 1 #coefficient for the right motor
        k_l = 2 #coefficient for the left motor
        k_c = 3 #coefficient for the center motor

        # activating 3 of the motors in certain value
        env.set_motor_ctrl([k_r * c * ctrl, k_l *  c * ctrl, k_c *  c * ctrl])

        # Getting the new observation
        observation = env.get_obs()
        print(env.sim.data.get_body_xmat('target_body'))


    # Taking a step and rendering the environment
    env.sim.step()
    env.render()