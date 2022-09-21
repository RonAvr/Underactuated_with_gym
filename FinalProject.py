import gym
import json
import numpy as np


def start_sim(motors_k):

    # Making the new environment
    env = gym.make("Example")

    # Resetting the environment
    observation, infos = env.reset(seed=42, return_info=True)

    # Resetting the position of the relevant joints
    qpos_reset = np.array([ 0, 0.25, 0, 0, 0.25, 0, 0, -0.2, 0, 0, 0, 0, 0, 0, 0, 0])
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
            c = i/root_loop
            ctrl = 0.00001
            k_r = motors_k[0] # coefficient for the right motor
            k_l = motors_k[1] # coefficient for the left motor
            k_c = motors_k[2] # coefficient for the center motor

            # activating 3 of the motors in certain value
            env.set_motor_ctrl([k_r * c * ctrl, k_l *  c * ctrl, k_c *  c * ctrl])

        # Getting target body pos
        target_body_pos = env.get_body_pos('target_body')
        pos_data.append(list(target_body_pos))

        # Adding the current time to the time_data array
        time_data.append(env.sim.data.time)

        # Taking a step and rendering the environment
        env.sim.step()
        env.render()

    env.close()
    # Data dict that contains the position data and the time data
    data = {
        'pos_data':pos_data,
        'time_data':time_data
    }

    # Saving the data into json file
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    print("Please enter the motors coefficient [right_motor, left_motor, center_motor]")
    print("Input for example - '1 2 1' ")
    print("for exit please enter - '-1' ")
    motors_k = input()

    while (motors_k != '-1'):
        motor_k_arr = motors_k.split(" ")
        motor_k_arr = [eval(i) for i in motor_k_arr]

        if(len(motor_k_arr) != 3):
            print("there was an error with your input pleas try again")
            motors_k = input()
            continue

        else:
            start_sim(motor_k_arr)

        print("Please enter the motors coefficient [right_motor, left_motor, center_motor]")
        print("for exit please enter - '-1' ")
        motors_k = input()

    print("Goodbye !")