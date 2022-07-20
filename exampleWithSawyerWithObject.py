import gym
import numpy as np
import matplotlib.pyplot as plt

# Making the new environment
env = gym.make("ExampleWithSawyerWithObject")
deg_to_rad = 0.0174532925

# Resetting the environment
observation, infos = env.reset(seed=42, return_info=True)

# Resetting the position of the relevant joints
# qpos_reset = np.array([0, 0, 0, 0, 0, 90 * deg_to_rad, 0, 0, 0.25, 0, 0, 0.25, 0, 0, -0.2, 0])
qpos_reset = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0.35, 0, 0, 0.35, 0, 0, -0.2, 0, 0, 0, 0, 0, 0, 0, 0])
env.set_reset(qpos_reset)
env.set_one_joint_value(5, 90 * deg_to_rad)

# Number of loops the simulation going to loop through
root_loop = 250
loops = 10 * root_loop

# How much the hand should go down
down_y_value = 0.08

# Moving the hand to the right position
for i in np.arange(0, down_y_value, 0.0001):
    joint_1 = env.sim.data.qpos[1]
    joint_5 = env.sim.data.qpos[5]
    env.set_one_joint_value(1 , i)
    env.set_one_joint_value(5, 90 * deg_to_rad - joint_1)
    env.sim.step()
    env.render()

# Closing the fingers
for i in range(loops):
    i += 1
    if (i%root_loop == 0):
        # Evaluating the value of the activation of the motors
        c = i/root_loop
        action = 0.0001

        # activating 3 of the motors in certain value
        env.set_motor_ctrl([c * action, c * action, c * action])

        # Getting the new observation
        # observation = env.get_obs()


    # Taking a step and rendering the environment
    env.sim.step()
    env.render()

# Moving the hand upwards
for i in np.arange(down_y_value, 0, -0.0001):
    joint_1 = env.sim.data.qpos[1]
    joint_5 = env.sim.data.qpos[5]
    env.set_one_joint_value(1, i)
    env.set_one_joint_value(5, 90 * deg_to_rad - joint_1)
    env.sim.step()
    env.render()