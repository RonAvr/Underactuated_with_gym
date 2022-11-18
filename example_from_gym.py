import gym
env = gym.make("Ant")
observation, info = env.reset(seed=42, return_info=True)
env.viewer_setup()
for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()
env.close()