import numpy as np
import math
import sys
from gym import utils
from gym.envs.mujoco import MuJocoPyEnv
from gym.spaces import Box


class Calibrate(MuJocoPyEnv, utils.EzPickle):
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
            self, "calibrate.xml", 5, observation_space=observation_space, **kwargs
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

    def set_reset(self, qpos_reset):
        """
        Args: The value of all the joints in the simulation
            qpos: 1D array, size of 9

        Returns: Resetting the simulation to the inputs values
        """

        # if (len(qpos_reset) != 9):
        #     raise ValueError('The qpos_reset array must be at size of 9')

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

    def get_body_pos(self, body_name):
        # The reference position where the camera is located
        ref_pos = [0.02, 0, 0.0625]

        # Getting the site position which located at the bottom of the target body
        site_pos = self.sim.data.get_site_xpos(body_name)

        # Getting the roll pitch and yaw of the body
        rpy = self.calc_rpy(body_name)

        # absolute x,y,z position
        abs_pos = site_pos - ref_pos

        # adding the roll pitch and yaw to the array
        abs_pos = np.append(abs_pos, rpy)

        return abs_pos

    def calc_rpy(self, body_name):
        # A function to convert orientation matrix to rpy
        # https://www.meccanismocomplesso.org/en/3d-rotations-and-euler-angles-in-python/

        tol = sys.float_info.epsilon * 10
        xmat = self.sim.data.get_geom_xmat(body_name)

        if abs(xmat[0, 0]) < tol and abs(xmat[1, 0]) < tol:
            eul1 = 0
            eul2 = math.atan2(-xmat[2, 0], xmat[0, 0])
            eul3 = math.atan2(-xmat[1, 2], xmat[1, 1])
        else:
            eul1 = math.atan2(xmat[1, 0], xmat[0, 0])
            sp = math.sin(eul1)
            cp = math.cos(eul1)
            eul2 = math.atan2(-xmat[2, 0], cp * xmat[0, 0] + sp * xmat[1, 0])
            eul3 = math.atan2(sp * xmat[0, 2] - cp * xmat[1, 2], cp * xmat[1, 1] - sp * xmat[0, 1])

        rpy = [eul1, eul2, eul3]

        return rpy

    def set_motor_ctrl(self, ctrl):
        """
        Args: The value of the control input for each of the motors
            ctrl: 1D array, size of 3

        Returns: Setting the motors value according to the ctrl array input
        """

        if (len(ctrl) != 3):
            raise ValueError('The ctrl array must be at size of 3')

        self.sim.data.ctrl[0] = ctrl[0]
        self.sim.data.ctrl[1] = ctrl[1]
        self.sim.data.ctrl[2] = ctrl[2]

    def get_sensor_data(self):
        return self.sim.data.sensordata

    def close_fingers(self):
        right_motor = 0.0001
        left_motor = 0.0001
        center_motor = 0.0001
        while(bool(right_motor and left_motor and center_motor)):
            sensor_data = self.get_sensor_data()
            if(sensor_data[0] != 0):
                right_motor = 0
            if(sensor_data[1] != 0):
                left_motor = 0
            if(sensor_data[2] != 0):
                center_motor = 0
            self.sim.step()
            self.render()

        return

    def move_motors(self, movement):
        first_movement = 0.0001 * np.array(movement)
        second_movement = -1 * np.array(first_movement)
        self.set_motor_ctrl(first_movement)
        self.sim.step()
        self.render()
        # self.set_motor_ctrl(second_movement)
        # self.sim.step()
        # self.render()