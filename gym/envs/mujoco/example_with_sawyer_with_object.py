import numpy as np

from gym import utils
from gym.envs.mujoco import MuJocoPyEnv
from gym.spaces import Box


class ExampleWithSawyerWithObject(MuJocoPyEnv, utils.EzPickle):
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
            "single_rgb_array",
            "single_depth_array",
        ],
        "render_fps": 100,
    }

    def __init__(self, **kwargs):
        observation_space = Box(
            low=-np.inf, high=np.inf, shape=(111,), dtype=np.float64
        )
        MuJocoPyEnv.__init__(
            self, "example_with_sawyer_with_object.xml", 5, observation_space=observation_space, **kwargs
        )
        utils.EzPickle.__init__(self)

    def step2(self, a):
        xposbefore = self.get_body_com("distal_r")[0]
        self.do_simulation(a, self.frame_skip)
        xposafter = self.get_body_com("distal_r")[0]

        self.renderer.render_step()

        forward_reward = (xposafter - xposbefore) / self.dt
        ctrl_cost = 0.5 * np.square(a).sum()
        contact_cost = (
            0.5 * 1e-3 * np.sum(np.square(np.clip(self.sim.data.cfrc_ext, -1, 1)))
        )
        survive_reward = 1.0
        reward = forward_reward - ctrl_cost - contact_cost + survive_reward
        state = self.state_vector()
        not_terminated = (
            np.isfinite(state).all() and state[2] >= 0.2 and state[2] <= 1.0
        )
        terminated = not not_terminated
        ob = self._get_obs()
        return (
            ob,
            reward,
            terminated,
            False,
            dict(
                reward_forward=forward_reward,
                reward_ctrl=-ctrl_cost,
                reward_contact=-contact_cost,
                reward_survive=survive_reward,
            ),
        )

    def _get_obs(self):
        return np.concatenate(
            [
                self.sim.data.qpos.flat,
                self.sim.data.qvel.flat,
            ]
        )

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(
            size=self.model.nq, low=-0.1, high=0.1
        )
        qvel = self.init_qvel + self.np_random.standard_normal(self.model.nv) * 0.1
        self.set_state(qpos, qvel)
        return self._get_obs()

    def viewer_setup(self):
        assert self.viewer is not None
        self.viewer.cam.distance = self.model.stat.extent * 0.5

    def controller(self):

        j1_target = -0.3

        k1 = 0.03

        j1 = - k1 * (self.sim.data.qpos[1] - (j1_target)) - k1 * self.sim.data.qvel[1]

        self.sim.data.ctrl[0] = j1

        self.sim.step()

    def set_reset(self, qpos_reset):
        """
        Args: The value of all the joints in the simulation
            qpos: 1D array, size of 9

        Returns: Resetting the simulation to the inputs values
        """

        # if (len(qpos_reset) != 16):
        #     raise ValueError('The qpos_reset array must be at size of 16')

        self.sim.data.qpos[:] = qpos_reset
        self.sim.data.qvel[:] = 0
        self.sim.step()
        self.sim.forward()

    def set_reset2(self, pos):
        self.sim.data.qpos[1] = self.sim.data.qpos[4] = pos
        self.sim.data.qpos[7] = -pos
        self.sim.data.qpos[:] = np.array([0, pos, 0, 0, pos, 0, 0, -pos, 0])
        self.sim.data.qvel[:] = 0
        self.sim.step()
        self.sim.forward()

    def get_obs(self):
        return np.concatenate(
            [
                self.sim.data.qpos,
                self.sim.data.qvel,
                self.sim.data.ctrl
            ]
        )

    def set_motor_ctrl(self, ctrl):
        """
        Args: The value of the control input for each of the motors
            ctrl: 1D array, size of 3

        Returns: Setting the motors value according to the ctrl array input
        """

        if (len(ctrl) != 3):
            raise ValueError('The ctrl array must be at size of 3')

        self.sim.data.ctrl[7] = ctrl[0]
        self.sim.data.ctrl[8] = ctrl[1]
        self.sim.data.ctrl[9] = ctrl[2]

    def set_one_motor_ctrl(self, motor,ctrl):
        """

        Args: The value of the control input for a motor
            motor: number
            ctrl: number

        Returns: Setting the motor value according to the input

        """

        if (motor > 9):
            raise ValueError('Invalid motor number')

        self.sim.data.ctrl[motor] = ctrl

    def set_one_joint_value(self, joint ,value):
        """

        Args: Setting a joint to a specific value
            joint: number
            value: number

        Returns: Setting the joint

        """

        # if (joint > 15):
        #     raise ValueError('Invalid motor number')

        self.sim.data.qpos[joint] = value