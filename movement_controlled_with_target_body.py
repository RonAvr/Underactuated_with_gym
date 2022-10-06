import gym
import json
import numpy as np

def save_data():
    # getting the data
    target_body_pos = env.get_body_pos('target_body')
    current_actuators_data = env.get_actuators_data()

    # adding the data
    pos_data.append(list(target_body_pos))
    actuators_data.append(current_actuators_data)
    time_data.append(env.sim.data.time)


# Making the new environment
env = gym.make("Move")

# Resetting the environment
observation, infos = env.reset(seed=42, return_info=True)

# Resetting the position of the relevant joints
qpos_reset = np.array([ 0, 0.17, 0, 0, 0.17, 0, 0, -0.17, 0, 0, 0, 0, 0, 0, 0, 0])
env.set_reset(qpos_reset)

# Number of loops the simulation going to loop through
root_loop = 1000
loop = 2 * root_loop

# array to store all the position data
pos_data = []
actuators_data = []
time_data = []

# Closing the fingers tothe target object
env.close_fingers()

for i in range(loop):
    # print('actuator force -',env.sim.data.actuator_force)
    # print('actuator length -',env.sim.data.actuator_length)
    # print('actuator moment -',env.sim.data.actuator_moment)
    # print('actuator velocity -',env.sim.data.actuator_velocity)

    save_data()
    if (i%root_loop == 0):
        # Activating the motors
        env.set_motor_ctrl([1,1,1])
        print(env.sim.data.ctrl)

    # Taking a step and rendering the environment
    env.sim.step()
    env.render()

print(type(actuators_data))

# Data dict that contains the position data and the time data
data = {
    'pos_data':pos_data,
    'actuators_data': actuators_data,
    'time_data':time_data
}
print(type(data))
# Saving the data into json file
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

