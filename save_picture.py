import gym
import json
import numpy as np
import imageio


def main_loop(iteration):
    def save_data():
        # getting the data
        target_body_pos = env.get_body_pos('target_body')
        current_actuators_data = env.get_actuators_data()
        current_joints_data = env.get_joints_data()

        # adding the data
        pos_data.append(list(target_body_pos))
        actuators_data.append(current_actuators_data)
        joints_data.append(current_joints_data)
        time_data.append(env.sim.data.time)

    # Making the new environment
    env = gym.make("Move")

    # Resetting the environment
    observation, infos = env.reset(seed=42, return_info=True)

    # Resetting the position of the relevant joints
    qpos_reset = np.array([0, 0.17, 0, 0, 0.17, 0, 0, -0.17, 0, 0, 0, 0, 0, 0, 0, 0])
    env.set_reset(qpos_reset)

    # Number of loops the simulation going to loop through
    root_loop = 50
    loop = 3 * root_loop

    # array to store all the position data
    pos_data = []
    actuators_data = []
    joints_data = []
    time_data = []

    # Closing the fingers tothe target object
    env.close_fingers()
    env.viewer_setup()
    motor_inputs = [[0.1, 0.1, 0.1],
                    [0.3, 0.1, 0.1],
                    [0.1, 0.3, 0.1],
                    [0.1, 0.1, 0.3],
                    [0.3, 0.3, 0.3]]
    for i in range(loop):
        save_data()
        env.set_motor_ctrl(motor_inputs[iteration])

        # Taking a step and rendering the environment
        env.sim.step()
        env.render()
        print(env.model.camera_names)
        # if i%50==0:
            # env.viewer.move_camera(1, 0.5, 2)
            # img = env.render(mode='rgb_array', width=1000, height=1000)
            # imageio.imwrite(f'{i}.png', img)

    # Data dict that contains the position data and the time data
    data = {
        'pos_data': pos_data,
        'actuators_data': actuators_data,
        'joints_data': joints_data,
        'time_data': time_data
    }

    # Saving the data into json file
    with open(f'TEST{iteration+1}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    for i in range(2):
        main_loop(i)
