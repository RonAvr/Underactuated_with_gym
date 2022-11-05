import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R


def motor_input1():
    fig, axs = plt.subplots(1, 5)
    right_motor = np.ones(150) * 0.1
    left_motor = np.ones(150) * 0.1
    center_motor = np.ones(150) * 0.1

    axs[0].plot(x, right_motor, x, left_motor, x, center_motor)
    axs[0].grid()
    axs[0].set(ylabel='Motor Input')
    axs[0].set_title('Input Number 1')

    axs[1].plot(x, right_motor*3, x, left_motor, x, center_motor)
    axs[1].grid()
    axs[1].set_title('Input Number 2')

    axs[2].plot(x, right_motor, x, left_motor*3, x, center_motor)
    axs[2].grid()
    axs[2].set_title('Input Number 3')
    axs[2].set(xlabel='Steps')


    axs[3].plot(x, right_motor, x, left_motor, x, center_motor*3)
    axs[3].grid()
    axs[3].set_title('Input Number 4')

    axs[4].plot(x, right_motor*3, x, left_motor*3, x, center_motor*3)
    axs[4].grid()
    axs[4].set_title('Input Number 5')
    fig.legend(['Right Motor', 'Left Motor', 'Center Motor'],
               loc="upper right")
    fig.suptitle('Position Motor', fontweight ="bold")
    plt.show()




x = np.arange(0, 150)
motor_input1()
