"""Extract a frame from the initial state of an environment for illustration purposes.
Lets user interactively move the camera, then takes a screenshot when ready."""

import argparse
import select
import sys
import time

import gym
import imageio
import mujoco_py
import numpy as np


def get_img(env_name, seed):
    env = gym.make(env_name)
    env.seed(int(seed))
    env.reset()

    print("Type save to save the image, step to take one timestep.")

    running = True
    while running:
        img = None
        while sys.stdin not in select.select([sys.stdin], [], [], 0)[0]:
            env.render()
            img = env.render(mode='rgb_array', width=1000, height=750)

        input = sys.stdin.readline().strip()
        if input == 'save':
            running = False
        elif input == 'step':
            action = tuple(np.zeros(space.shape) for space in env.action_space.spaces)
            env.step(action)
        else:
            print(f"Unrecognized command '{input}'")

    return img


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default="Move", help="environment name")
    parser.add_argument('--seed', type=int, default=time.time())
    parser.add_argument('--out', type=str, default="frame.png", help="path to save figure")
    args = parser.parse_args()

    img = get_img(args.env, args.seed)
    imageio.imwrite(args.out, img)

if __name__ == '__main__':
    main()