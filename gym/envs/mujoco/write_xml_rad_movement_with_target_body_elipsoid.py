g = 0
deg_to_rad = 0.0174532925

motor_damping = 0.0000000001
motor_stiffness = 0.0000000001
proximal_damping = 0.001
proximal_stiffness = 0.000000001
distal_damping = 0.001
distal_stiffness = 0.000000001

# Motors coefficients
motor_damping = motor_damping
motor_stiffness = motor_stiffness
motor_joint_range = f"{-45 * deg_to_rad} {45 * deg_to_rad}"
motor_lower_range = -10
motor_upper_range = 10

# Swivel-proximal joint coefficients
swivel_proximal_damping = proximal_damping
swivel_proximal_stiffness = proximal_stiffness
swivel_proximal_joint_range = f"{-45 * deg_to_rad} {45 * deg_to_rad}"

# Proximal-distal joint coefficients
proximal_distal_damping = distal_damping
proximal_distal_stiffness = distal_stiffness
proximal_distal_joint_range = f"{-30 * deg_to_rad} {30 * deg_to_rad}"

# Tendons coefficients
tendon_stiffness = 1000
tendon_range = 0.1
tendon_width = 0.001

# camera pos
camera_x = 0.025
camera_y = 0
camera_z = 0.0625

# Object to grab parameters
width = 0.005
length = 0.01
height = 0.07

center_off_body_z = 0.21
x_pos = 0.019
y_pos = 0
z_pos = center_off_body_z - height / 2

MODEL_XML = f"""
<?xml version="1.0" ?>
<mujoco>
    <!-- meshdir - STL files path -->
    <compiler meshdir="/home/ron/PycharmProjects/pythonProject/meshes/" angle="radian"/>
    
   <asset>
       <texture type="skybox" builtin="gradient" rgb1="1 1 1" rgb2="0 0 0" width="512" height="512"/>
        <mesh file="base_link.STL"/>
        <mesh file="proximal_O.STL" scale="0.00100 0.00100 0.00100"/>
        <mesh file="distal_O.STL" scale="0.00100 0.00100 0.00100"/>
        <mesh file="swivel_1.STL"/>
   </asset>
   
   <option gravity="0 0 {g}" integrator="RK4"/>

   <worldbody>

      <light diffuse="1 1 1" pos="0 0 300" dir="0 0 -1"/>

      <body name="base_link">
          <site name="camera_pos" pos="{camera_x} {camera_y} {camera_z}" size="0.0015"/>
          <geom type="mesh" mesh="base_link"/>

          <!-- Creating the right arm with its motor -->
          <body name="Right motor">
              <site name="s11" pos="0.06 0.025 0.04" size="0.0015"/>
              <geom name="geom1" type="sphere" pos="0.06 0.025 0.04" size="0.005"/>
              <joint name="joint_1" type="hinge" pos="0.045 0.0125 0.04" axis="0 1 0" limited="true" range="{motor_joint_range}" stiffness="{motor_stiffness}" damping="{motor_damping}"/>
          </body>
          <body name="swivel_r" pos="0.05 0.025 0.0625" euler="0 0 {30 * deg_to_rad}" >
              <geom name="swivel_r" type="mesh" mesh="swivel_1"/>
              <body name="proximal_r" pos="0.0038 0 0.0475">
                  <joint name="swivel_proximal_r" type="hinge" axis="0 1 0" pos="0.006 0 -0.03" limited="true" range="{swivel_proximal_joint_range}" stiffness="{swivel_proximal_stiffness}" damping="{swivel_proximal_damping}"/>
                  <site name="s12" pos="0.007 0 -0.04" size="0.0015"/>
                  <geom name="12_cylinder" type="cylinder" size="0.005 0.01" pos="0.005 0 -0.029" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
                  <site name="s131" pos="0.0035 0 -0.035" size="0.0015"/>
                  <site name="s13" pos="0 0 -0.03" size="0.0015"/>
                  <geom name="13_cylinder" type="cylinder" size="0.004 0.01" pos="0.0014 0 -0.0175" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
                  <site name="s132" pos="0.0035 0 -0.023" size="0.0015"/>
                  <site name="s14" pos="0.005 0 -0.012" size="0.0015"/>
                  <site name="s15" pos="0 0 0.014" size="0.0015"/>
                  <geom name="14_cylinder" type="cylinder" size="0.004 0.01" pos="-0.00575 0 0.01675" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
                  <geom name="15_cylinder" type="cylinder" size="0.01 0.01" pos="-0.007 0 0.032" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
                  <geom name="proximal_r" type="mesh" mesh="proximal_O" pos="-0.01 -0.008 0.045" euler="{90  * deg_to_rad} {180 * deg_to_rad} {-150 * deg_to_rad}"/>
                  <site name="s16" pos="-0.014 0 0.021" size="0.0015"/>
                  <body name="distal_r" pos="-0.027 0 0.068" euler="0 {65 * deg_to_rad} 0">
                      <joint name="proximal_distal_r" type="hinge" axis="0 1 0" pos="0.041 0 0.0025" limited="true" range="{proximal_distal_joint_range}" stiffness="{proximal_distal_stiffness}" damping="{proximal_distal_damping}"/>
                      <geom name="distal_r" type="mesh" mesh="distal_O" pos="-0.015 0.015 0.015" euler="{-90 * deg_to_rad} {90 * deg_to_rad} 0"/>
                      <site name="s17" pos="0.022 0 0.009" size="0.0015"/>
                      <site name="right_sensor" pos="-0.01 0 -0.02" size="0.015" rgba="0 0 0 0"/>
                  </body>
              </body>
          </body>

           <!-- Creating the left arm with its motor -->
          <body name="Left Motor">
              <site name="s21" pos="0.06 -0.025 0.04" size="0.0015"/>
              <geom name="geom2" type="sphere" pos="0.06 -0.025 0.04" size="0.005"/>
              <joint name="joint_2" type="hinge" pos="0.045 -0.025 0.04" axis="0 1 0" limited="true" range="{motor_joint_range}" stiffness="{motor_stiffness}" damping="{motor_damping}"/>
          </body>
          <body name="swivel_l" pos="0.05 -0.025 0.0625" euler="0 0 {-30 * deg_to_rad}">
              <geom type="mesh" mesh="swivel_1"/>
              <body name="proximal_l" pos="0.0038 0 0.0475">
                  <joint name="swivel_proximal_l" type="hinge" axis="0 1 0" pos="0.006 0 -0.03" limited="true" range="{swivel_proximal_joint_range}" stiffness="{swivel_proximal_stiffness}" damping="{swivel_proximal_damping}"/>
                  <site name="s22" pos="0.007 0 -0.04" size="0.0015"/>
                  <geom name="22_cylinder" type="cylinder" size="0.005 0.01" pos="0.005 0 -0.029" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
                  <site name="s231" pos="0.0035 0 -0.035" size="0.0015"/>
                  <site name="s23" pos="0 0 -0.03" size="0.0015"/>
                  <geom name="23_cylinder" type="cylinder" size="0.004 0.01" pos="0.0014 0 -0.0175" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
                  <site name="s232" pos="0.0035 0 -0.023" size="0.0015"/>
                  <site name="s24" pos="0.005 0 -0.012" size="0.0015"/>
                  <site name="s25" pos="0 0 0.014" size="0.0015"/>
                  <geom name="24_cylinder" type="cylinder" size="0.004 0.01" pos="-0.00575 0 0.01675" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
                  <geom name="25_cylinder" type="cylinder" size="0.01 0.01" pos="-0.007 0 0.032" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
                  <geom name="proximal_l" type="mesh" mesh="proximal_O" pos="-0.01 -0.008 0.045" euler="{90 * deg_to_rad} {180 * deg_to_rad} {-150 * deg_to_rad}"/>
                  <site name="s26" pos="-0.014 0 0.021" size="0.0015"/>
                  <body name="distal_l" pos="-0.027 0 0.068" euler="0 {65 * deg_to_rad} 0">
                      <joint name="proximal_distal_l" type="hinge" axis="0 1 0" pos="0.041 0 0.0025" limited="true" range="{proximal_distal_joint_range}" stiffness="{proximal_distal_stiffness}" damping="{proximal_distal_damping}"/>
                      <geom name="distal_l" type="mesh" mesh="distal_O" pos="-0.015 0.015 0.015" euler="{-90 * deg_to_rad} {90 * deg_to_rad} 0"/>
                      <site name="s27" pos="0.022 0 0.009" size="0.0015"/>
                      <site name="left_sensor" pos="-0.01 0 -0.02" size="0.015" rgba="0 0 0 0"/>
                  </body>
              </body>
          </body>

          <!-- Creating the center arm with its motor -->
          <body name="Center Motor">
              <site name="s31" pos="-0.03 0 0.035" size="0.0015"/>
              <geom name="geom3" type="sphere" pos="-0.03 0 0.035" size="0.005"/>
              <joint name="joint_3" type="hinge" pos="-0.045 0 0.035" axis="0 1 0" limited="true" range="{motor_joint_range}" stiffness="{motor_stiffness}" damping="{motor_damping}"/>
          </body>
          <body name="proximal_c" pos="-0.0138 0 0.1105">
              <joint name="swivel_proximal_c" type="hinge" axis="0 1 0" pos="-0.016 -0.01 -0.029" limited="true" range="{swivel_proximal_joint_range}" stiffness="{swivel_proximal_stiffness}" damping="{swivel_proximal_damping}"/>
              <geom name="35_cylinder" type="cylinder" size="0.01 0.01" pos="-0.003 0 0.032" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
              <geom name="proximal_c" type="mesh" mesh="proximal_O" pos="0 0.008 0.045" euler="{90 * deg_to_rad} 0 {-150 * deg_to_rad}"/>
              <site name="s32" pos="-0.016 0 -0.04" size="0.0015"/>
              <geom name="32_cylinder" type="cylinder" size="0.005 0.01" pos="-0.018 0 -0.029" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
              <site name="s331" pos="-0.0165 0 -0.035" size="0.0015"/>
              <site name="s33" pos="-0.023 0 -0.03" size="0.0015"/>
              <geom name="33_cylinder" type="cylinder" size="0.004 0.01" pos="-0.0115 0 -0.0175" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
              <site name="s332" pos="-0.0165 0 -0.023" size="0.0015"/>
              <site name="s34" pos="-0.018 0 -0.012" size="0.0015"/>
              <site name="s35" pos="-0.012 0 0.014" size="0.0015"/>
              <geom name="34_cylinder" type="cylinder" size="0.004 0.01" pos="-0.0045 0 0.01675" rgba=".3 .9 .3 .4" euler="{90 * deg_to_rad} 0 0"/>
              <site name="s36" pos="0.0025 0 0.021" size="0.0015"/>
              <body name="distal_c" pos="0.02 0 0.066" euler="0 {120 * deg_to_rad} 0">
                  <joint name="proximal_distal_c" type="hinge" axis="0 1 0" pos="0.041 0 -0.0025" limited="true" range="{proximal_distal_joint_range}" stiffness="{proximal_distal_stiffness}" damping="{proximal_distal_damping}"/>
                  <geom type="mesh" mesh="distal_O" pos="-0.015 -0.015 -0.015" euler="{90 * deg_to_rad} {90 * deg_to_rad} 0"/>
                  <site name="s37" pos="0.022 0 -0.01" size="0.0015"/>
                  <site name="center_sensor" pos="-0.01 0 0.02" size="0.015" rgba="0 0 0 0"/>
              </body>
          </body>
      </body>
    <body name="target_body">
        <geom pos="{x_pos} {y_pos} {z_pos}" size="{width} {length} {height}" type="ellipsoid" name="target_body"/>
        <site name="target_body" pos="{x_pos} {y_pos} {z_pos - height}" size="0.0015"/>
        <joint type="free"/>
    </body>
   </worldbody>

   <tendon> <!-- Creating the tendon's path according to the sites -->
      <spatial name="tendon_r" width="{tendon_width}" rgba=".95 .3 .3 1" limited="true" range="0 {tendon_range}" stiffness="{tendon_stiffness}">
          <site site="s11"/>
          <site site="s12"/>
          <site site="s131"/>
          <geom geom="12_cylinder"/>
          <site site="s132"/>
          <geom geom="13_cylinder"/>
          <site site="s14"/>
          <site site="s15"/>
          <geom geom="14_cylinder"/>
          <site site="s16"/>
          <geom geom="15_cylinder"/>
          <site site="s17"/>
      </spatial>
      <spatial name="tendon_l" width="{tendon_width}" rgba=".95 .3 .3 1" limited="true" range="0 {tendon_range}" stiffness="{tendon_stiffness}">
          <site site="s21"/>
          <site site="s22"/>
          <site site="s231"/>
          <geom geom="22_cylinder"/>
          <site site="s232"/>
          <geom geom="23_cylinder"/>
          <site site="s24"/>
          <site site="s25"/>
          <geom geom="24_cylinder"/>
          <site site="s26"/>
          <geom geom="25_cylinder"/>
          <site site="s27"/>
      </spatial>
      <spatial name="tendon_c" width="{tendon_width}" rgba=".95 .3 .3 1" limited="true" range="0 {tendon_range}" stiffness="{tendon_stiffness}">
          <site site="s31"/>
          <site site="s32"/>
          <site site="s331"/>
          <geom geom="32_cylinder"/>
          <site site="s332"/>
          <geom geom="33_cylinder"/>
          <site site="s34"/>
          <site site="s35"/>
          <geom geom="34_cylinder"/>
          <site site="s36"/>
          <geom geom="35_cylinder"/>
          <site site="s37"/>
      </spatial>
   </tendon>

   <actuator> <!-- Adding motors to the relevant joints -->
        <position joint="joint_1" name="swivel_proximal_r_motor" gear="1" ctrllimited="true" ctrlrange="{motor_lower_range} {motor_upper_range}" kp="1"/>

        <position joint="joint_2" name="swivel_proximal_l_motor" gear="1" ctrllimited="true" ctrlrange="{motor_lower_range} {motor_upper_range}"/>

        <position joint="joint_3" name="swivel_proximal_c_motor" gear="1" ctrllimited="true" ctrlrange="{motor_lower_range} {motor_upper_range}"/>
    </actuator>

    <contact>
        <exclude name="exclude1" body1="proximal_c" body2="base_link"/>
        <exclude name="exclude2" body1="Center Motor" body2="base_link"/>
        <exclude name="exclude3" body1="Left Motor" body2="base_link"/>

        <exclude name="exclude5" body1="swivel_l" body2="base_link"/>
        <exclude name="exclude6" body1="swivel_r" body2="base_link"/>
        <exclude name="exclude7" body1="proximal_r" body2="swivel_r"/>
        <exclude name="exclude8" body1="proximal_l" body2="swivel_l"/>
        <exclude name="exclude9" body1="Right motor" body2="base_link"/>

    </contact>
    
    <sensor>
        <touch name="touchsensor_right" site="right_sensor" />
        <touch name="touchsensor_left" site="left_sensor" />
        <touch name="touchsensor_center" site="center_sensor" />
    </sensor>
    
</mujoco>

"""

with open("./assets/movement_elipsoid.xml", "w") as f:
    f.write(MODEL_XML)

f.close()