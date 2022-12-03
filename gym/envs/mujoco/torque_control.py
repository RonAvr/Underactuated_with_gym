import numpy as np
import math
import sys
from gym import utils
from gym.envs.mujoco import MuJocoPyEnv
from gym.spaces import Box
from scipy.spatial.transform import Rotation as R


class Torque(MuJocoPyEnv, utils.EzPickle):
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
            self, "torque.xml", 5, observation_space=observation_space, **kwargs
        )
        utils.EzPickle.__init__(self)

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

        self.sim.data.qpos[:] = qpos_reset
        self.sim.data.qvel[:] = 0
        self.sim.step()
        self.sim.forward()

    def get_actuators_data(self):
        """
        Returns: All actuators data
        """
        actuator_force = self.sim.data.actuator_force.tolist()
        actuator_length = self.sim.data.actuator_length.tolist()
        actuator_moment = self.sim.data.actuator_moment.tolist()
        actuator_velocity = self.sim.data.actuator_velocity.tolist()
        actuators_data = {
            'actuator_force' : actuator_force,
            'actuator_length' : actuator_length,
            'actuator_moment' : actuator_moment,
            'actuator_velocity' : actuator_velocity
        }

        return actuators_data

    def get_joints_data(self):
        """
        Returns: All joints data
        """
        # Getting right joins vel and pos
        proximal_right_joint_pos = self.sim.data.get_joint_qpos('swivel_proximal_r')
        proximal_right_joint_vel = self.sim.data.get_joint_qvel('swivel_proximal_r')
        distal_right_joint_pos = self.sim.data.get_joint_qpos('proximal_distal_r')
        distal_right_joint_vel = self.sim.data.get_joint_qvel('proximal_distal_r')

        # Getting left joins vel and pos
        proximal_left_joint_pos = self.sim.data.get_joint_qpos('swivel_proximal_l')
        proximal_left_joint_vel = self.sim.data.get_joint_qvel('swivel_proximal_l')
        distal_left_joint_pos = self.sim.data.get_joint_qpos('proximal_distal_l')
        distal_left_joint_vel = self.sim.data.get_joint_qvel('proximal_distal_l')

        # Getting center joins vel and pos
        proximal_center_joint_pos = self.sim.data.get_joint_qpos('swivel_proximal_c')
        proximal_center_joint_vel = self.sim.data.get_joint_qvel('swivel_proximal_c')
        distal_center_joint_pos = self.sim.data.get_joint_qpos('proximal_distal_c')
        distal_center_joint_vel = self.sim.data.get_joint_qvel('proximal_distal_c')

        joints_data = {
            'right_proximal' : [proximal_right_joint_pos, proximal_right_joint_vel],
            'right_distal' : [distal_right_joint_pos, distal_right_joint_vel],
            'left_proximal' : [proximal_left_joint_pos, proximal_left_joint_vel],
            'left_distal' : [distal_left_joint_pos, distal_left_joint_vel],
            'center_proximal' : [proximal_center_joint_pos, proximal_center_joint_vel],
            'center_distal' : [distal_center_joint_pos, distal_center_joint_vel]
        }

        return joints_data

    def get_body_pos(self, body_name):
        """
        Args:
            body_name: the name of the body, str

        Returns: the position of the body
        """
        # The reference position where the camera is located
        ref_pos = self.sim.data.get_site_xpos('camera_pos')
        # ref_pos = [0.025, 0, 0.0625]

        # Getting the site position which located at the bottom of the target body
        site_pos = self.sim.data.get_site_xpos(body_name)

        # Getting the roll pitch and yaw of the body
        quat = self.calc_quat(body_name)

        # relative x,y,z position
        rel_pos = site_pos - ref_pos

        # adding the quat to the x,y,z position
        quat = list(quat)
        rel_pos = list(rel_pos)
        rel_pos.append(quat)

        return rel_pos

    def calc_quat(self, body_name):
        """
        Args:
            body_name: the name of the body, str

        Returns: the quat array of the body
        """
        xmat = self.sim.data.get_geom_xmat(body_name)

        r = R.from_matrix(xmat)

        r = r.as_quat()

        return r

    def set_motor_ctrl(self, ctrl):
        """
        Args: The value of the control input for each of the motors
            ctrl: 1D array, size of 3

        Returns: Setting the motors value according to the ctrl array input
        """

        if (len(ctrl) != 3):
            raise ValueError('The ctrl array must be at size of 3')

        calibration = 0.001
        self.sim.data.ctrl[0] = calibration * ctrl[0]
        self.sim.data.ctrl[1] = calibration * ctrl[1]
        self.sim.data.ctrl[2] = calibration * ctrl[2]

    def get_sensor_data(self):
        """
        Returns: all the data from the sensors in the model
        """
        return self.sim.data.sensordata

    def close_fingers(self):
        """
        This method is for closing the fingers on the target body
        """
        right_motor = 0.1
        left_motor = 0.1
        center_motor = 0.1
        while(bool(right_motor and left_motor and center_motor)):
            self.set_motor_ctrl([right_motor, left_motor, center_motor])
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

