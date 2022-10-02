import gym
import json
import numpy as np

def main_loop():
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
            env.move_motors(motor_k_arr)
            env.render()

        print("Please enter the motors coefficient [right_motor, left_motor, center_motor]")
        print("for exit please enter - '-1' ")
        motors_k = input()

    print("Goodbye !")




# Making the new environment
env = gym.make("Calibrate")

# Resetting the environment
observation, infos = env.reset(seed=42, return_info=True)

# Resetting the position of the relevant joints
qpos_reset = np.array([ 0, 0.25, 0, 0, 0.25, 0, 0, -0.15, 0])
env.set_reset(qpos_reset)

# Number of loops the simulation going to loop through
root_loop = 1000
loop = 100 * root_loop

# array to store all the position data
pos_data = []
time_data = []

# Closing the fingers tothe target object



for i in range(loop):
    if ( i == 1000):
        x = 0.0001
        movement = [1*x, 0, 0]
        env.set_motor_ctrl(movement)
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

