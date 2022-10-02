import gym
import json
import numpy as np

# Making the new environment
env = gym.make("Torque")

# Resetting the environment
observation, infos = env.reset(seed=42, return_info=True)

# Resetting the position of the relevant joints
qpos_reset = np.array([ 0, 0.25, 0, 0, 0.25, 0, 0, -0.15, 0, 0, 0, 0, 0, 0, 0, 0])
env.set_reset(qpos_reset)

# Number of loops the simulation going to loop through
root_loop = 1000
loop = 8 * root_loop

# array to store all the position data
pos_data = []
time_data = []

for i in range(loop):

    if (i%root_loop == 0):
        # Evaluating the value of the activation of the motors
        env.set_motor_ctrl([1,0,0])

    # Getting target body pos
    target_body_pos = env.get_body_pos('target_body')
    pos_data.append(list(target_body_pos))

    # Adding the current time to the time_data array
    time_data.append(env.sim.data.time)

    # Taking a step and rendering the environment
    env.sim.step()
    env.render()

# Data dict that contains the position data and the time data
data = {
    'pos_data':pos_data,
    'time_data':time_data
}

# Saving the data into json file
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

