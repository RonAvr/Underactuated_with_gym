g = 0
deg_to_rad = 0.0174532925

damping = 0.00001
stiffness = 0.00001

# Motors coefficients
motor_damping = damping
motor_stiffness = stiffness
motor_joint_range = f"{-45 * deg_to_rad} {45 * deg_to_rad}"
motor_lower_range = -0.035
motor_upper_range = 0.04

# Swivel-proximal joint coefficients
swivel_proximal_damping = damping
swivel_proximal_stiffness = stiffness
swivel_proximal_joint_range = f"{-45 * deg_to_rad} {45 * deg_to_rad}"

# Proximal-distal joint coefficients
proximal_distal_damping = damping
proximal_distal_stiffness = stiffness
proximal_distal_joint_range = f"{-30 * deg_to_rad} {30 * deg_to_rad}"

# Tendons coefficients
tendon_stiffness = 1000
tendon_range = 0.1

MODEL_XML = f"""
<mujoco model="sawyer">
	<compiler angle="radian"/>

    <asset>
    	<mesh file="sawyer/base.stl" name="base"/>
    	<mesh file="sawyer/l0.stl" name="l0"/>
    	<mesh file="sawyer/head.stl" name="head"/>
    	<mesh file="sawyer/l1.stl" name="l1"/>
    	<mesh file="sawyer/l2.stl" name="l2"/>
    	<mesh file="sawyer/l3.stl" name="l3"/>
    	<mesh file="sawyer/l4.stl" name="l4"/>
    	<mesh file="sawyer/l5.stl" name="l5"/>
    	<mesh file="sawyer/l6.stl" name="l6"/>

		<!-- Adding skybox for better visualisation -->
		<texture type="skybox" builtin="gradient" rgb1="1 1 1" rgb2="0 0 0" width="512" height="512"/>

		<!-- STLs for the arm -->
		<mesh file="sawyer/base_link.STL"/>
        <mesh file="sawyer/proximal_O.STL" scale="0.00100 0.00100 0.00100"/>
        <mesh file="sawyer/distal_O.STL" scale="0.00100 0.00100 0.00100"/>
        <mesh file="sawyer/swivel_1.STL"/>

    </asset>

   <option gravity="0 0 {g}"/>

    <worldbody>
    	<body name="base" pos="0 0 0">
			<!-- robot view -->
			<camera mode="fixed" name="robotview" pos="1.0 0 0.4" quat="0.653 0.271 0.271 0.653"/>
    		<inertial diaginertia="0 0 0" mass="0" pos="0 0 0"/>
            <!-- mount attached here -->
    		<body name="right_arm_base_link" pos="0 0 0">
    			<inertial diaginertia="0.00740351 0.00681776 0.00672942" mass="2.0687" pos="-0.0006241 -2.8025e-05 0.065404" quat="-0.209285 0.674441 0.227335 0.670558"/>
    			<geom conaffinity="0" contype="0" group="1" mesh="base" type="mesh" name="base_vis" rgba="0.5 0.1 0.1 1"/>
    			<geom pos="0 0 0.12" rgba="0.5 0.1 0.1 1" size="0.08 0.12" type="cylinder" name="base_col"/>
    			<body name="right_l0" pos="0 0 0.08">
    				<inertial diaginertia="0.0651588 0.0510944 0.0186218" mass="5.3213" pos="0.024366 0.010969 0.14363" quat="0.894823 0.00899958 -0.170275 0.412573"/>
    				<joint axis="0 0 1" limited="true" name="right_j0" pos="0 0 0" range="-3.0503 3.0503"/>
    				<geom conaffinity="0" contype="0" group="1" mesh="l0" type="mesh" name="link0_visual" rgba="0.5 0.1 0.1 1"/>
    				<geom pos="0.08 0 0.23" rgba="0.5 0.1 0.1 1" size="0.07" name="link0_collision"/>
    				<body name="head" pos="0 0 0.2965">
    					<inertial diaginertia="0.0118334 0.00827089 0.00496574" mass="1.5795" pos="0.0053207 -2.6549e-05 0.1021" quat="0.999993 7.08405e-05 -0.00359857 -0.000626247"/>
    					<!--Don't want to control the head joint so remove it from the kinematic tree-->
    					<!--<joint axis="0 0 1" limited="true" name="head_pan" pos="0 0 0" range="-5.0952 0.9064"/>-->
    					<geom conaffinity="0" contype="0" group="1" mesh="head" type="mesh" name="head_visual" rgba="0.5 0.1 0.1 1"/>
    					<geom pos="0 0 0.08" rgba="0.5 0.1 0.1 1" size="0.018" name="head_collision"/>
    					<body name="screen" pos="0.03 0 0.105" quat="0.5 0.5 0.5 0.5">
    						<inertial diaginertia="1e-08 1e-08 1e-08" mass="0.0001" pos="0 0 0"/>
    						<geom conaffinity="0" contype="0" group="1" size="0.12 0.07 0.001" type="box" name="screen_visual" rgba="0.2 0.2 0.2 1"/>
    						<geom rgba="0.2 0.2 0.2 1" size="0.001" name="screen_collision"/>
    					</body>
    					<body name="head_camera" pos="0.0228027 0 0.216572" quat="0.342813 -0.618449 0.618449 -0.342813">
    						<inertial diaginertia="0 0 0" mass="0" pos="0.0228027 0 0.216572" quat="0.342813 -0.618449 0.618449 -0.342813"/>
    					</body>
    				</body>
    				<body name="right_torso_itb" pos="-0.055 0 0.22" quat="0.707107 0 -0.707107 0">
    					<inertial diaginertia="1e-08 1e-08 1e-08" mass="0.0001" pos="0 0 0"/>
    				</body>
    				<body name="right_l1" pos="0.081 0.05 0.237" quat="0.5 -0.5 0.5 0.5">
    					<inertial diaginertia="0.0224339 0.0221624 0.0097097" mass="4.505" pos="-0.0030849 -0.026811 0.092521" quat="0.424888 0.891987 0.132364 -0.0794296"/>
    					<joint axis="0 0 1" limited="true" name="right_j1" pos="0 0 0" range="-3.8095 2.2736"/>
    					<geom conaffinity="0" contype="0" group="1" mesh="l1" type="mesh" name="link1_visual" rgba="0.5 0.1 0.1 1"/>
    					<geom pos="0 0 0.1225" rgba="0.5 0.1 0.1 1" size="0.07" name="link1_collision"/>
    					<body name="right_l2" pos="0 -0.14 0.1425" quat="0.707107 0.707107 0 0">
    						<inertial diaginertia="0.0257928 0.025506 0.00292515" mass="1.745" pos="-0.00016044 -0.014967 0.13582" quat="0.707831 -0.0524761 0.0516007 0.702537"/>
    						<joint axis="0 0 1" limited="true" name="right_j2" pos="0 0 0" range="-3.0426 3.0426"/>
    						<geom conaffinity="0" contype="0" group="1" mesh="l2" type="mesh" name="link2_visual" rgba="0.5 0.1 0.1 1"/>
    						<geom pos="0 0 0.08" rgba="0.5 0.1 0.1 1" size="0.06 0.17" type="cylinder" name="link2_collision"/>
    						<body name="right_l3" pos="0 -0.042 0.26" quat="0.707107 -0.707107 0 0">
    							<inertial diaginertia="0.0102404 0.0096997 0.00369622" mass="2.5097" pos="-0.0048135 -0.0281 -0.084154" quat="0.902999 0.385391 -0.0880901 0.168247"/>
    							<joint axis="0 0 1" limited="true" name="right_j3" pos="0 0 0" range="-3.0439 3.0439"/>
    							<geom conaffinity="0" contype="0" group="1" mesh="l3" type="mesh" name="link3_visual" rgba="0.5 0.1 0.1 1"/>
    							<geom pos="0 -0.01 -0.12" rgba="0.5 0.1 0.1 1" size="0.06" name="link3_collision"/>
    							<body name="right_l4" pos="0 -0.125 -0.1265" quat="0.707107 0.707107 0 0">
    								<inertial diaginertia="0.0136549 0.0135493 0.00127353" mass="1.1136" pos="-0.0018844 0.0069001 0.1341" quat="0.803612 0.031257 -0.0298334 0.593582"/>
    								<joint axis="0 0 1" limited="true" name="right_j4" pos="0 0 0" range="-2.9761 2.9761"/>
    								<geom conaffinity="0" contype="0" group="1" mesh="l4" type="mesh" name="link4_visual" rgba="0.5 0.1 0.1 1"/>
    								<geom pos="0 0 0.11" rgba="0.5 0.1 0.1 1" size="0.045 0.15" type="cylinder" name="link4_collision"/>
    								<body name="right_arm_itb" pos="-0.055 0 0.075" quat="0.707107 0 -0.707107 0">
    									<inertial diaginertia="1e-08 1e-08 1e-08" mass="0.0001" pos="0 0 0"/>
    								</body>
    								<body name="right_l5" pos="0 0.031 0.275" quat="0.707107 -0.707107 0 0">
    									<inertial diaginertia="0.00474131 0.00422857 0.00190672" mass="1.5625" pos="0.0061133 -0.023697 0.076416" quat="0.404076 0.9135 0.0473125 0.00158335"/>
    									<joint axis="0 0 1" limited="true" name="right_j5" pos="0 0 0" range="-2.9761 2.9761" damping="0.2"/>
    									<geom conaffinity="0" contype="0" group="1" mesh="l5" type="mesh" name="link5_visual" rgba="0.5 0.1 0.1 1"/>
    									<geom pos="0 0 0.1" rgba="0.5 0.1 0.1 1" size="0.06" name="link5_collision"/>
    									<body name="right_hand_camera" pos="0.039552 -0.033 0.0695" quat="0.707107 0 0.707107 0">
    										<inertial diaginertia="0 0 0" mass="0" pos="0.039552 -0.033 0.0695" quat="0.707107 0 0.707107 0"/>
    									</body>
    									<body name="right_wrist" pos="0 0 0.10541" quat="0.707107 0.707107 0 0">
    										<inertial diaginertia="0 0 0" mass="0" pos="0 0 0.10541" quat="0.707107 0.707107 0 0"/>
    									</body>
    									<body name="right_l6" pos="0 -0.11 0.1053" quat="0.0616248 0.06163 -0.704416 0.704416">
    										<inertial diaginertia="0.000360258 0.000311068 0.000214974" mass="0.3292" pos="-8.0726e-06 0.0085838 -0.0049566" quat="0.479044 0.515636 -0.513069 0.491322"/>
    										<joint axis="0 0 1" limited="true" name="right_j6" pos="0 0 0" range="-4.7124 4.7124" damping="0.1"/>
    										<geom conaffinity="0" contype="0" group="1" mesh="l6" type="mesh" name="link6_visual" rgba="0.5 0.1 0.1 1"/>
    										<geom pos="0 0.015 -0.01" rgba="0.5 0.1 0.1 1" size="0.055 0.025" type="cylinder" name="link6_collision"/>
    										<body name="right_hand" pos="0 0 0.024" quat="0.707105 0 0 0.707108">
												<!-- This camera points out from the eef. -->
                								<camera mode="fixed" name="eye_in_hand" pos="0.05 0 0" quat="0 0.707108 0.707108 0" fovy="75"/>
    											<!-- To add gripper -->





											  <body name="base_link">
												  <geom type="mesh" mesh="base_link"/>

												  <!-- Creating the right arm with its motor -->
												  <body name="Right motor">
													  <site name="s11" pos="0.06 0.025 0.035" size="0.0015"/>
													  <geom name="geom1" type="sphere" pos="0.06 0.025 0.04" size="0.005"/>
													  <joint name="joint_1" type="hinge" pos="0.045 0.0125 0.04" axis="0 1 0" limited="true" range="-0.7853981624999999 0.7853981624999999" stiffness="1e-05" damping="1e-05"/>
												  </body>
												  <body name="swivel_r" pos="0.05 0.025 0.0625" euler="0 0 0.523598775" >
													  <geom name="swivel_r" type="mesh" mesh="swivel_1"/>
													  <body name="proximal_r" pos="0.0038 0 0.0475">
														  <joint name="swivel_proximal_r" type="hinge" axis="0 1 0" pos="0.006 0 -0.03" limited="true" range="-0.7853981624999999 0.7853981624999999" stiffness="1e-05" damping="1e-05"/>
														  <site name="s12" pos="0.007 0 -0.04" size="0.0015"/>
														  <geom name="12_cylinder" type="cylinder" size="0.005 0.01" pos="0.005 0 -0.029" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
														  <site name="s131" pos="0.0035 0 -0.035" size="0.0015"/>
														  <site name="s13" pos="0 0 -0.03" size="0.0015"/>
														  <geom name="13_cylinder" type="cylinder" size="0.004 0.01" pos="0.0014 0 -0.0175" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
														  <site name="s132" pos="0.0035 0 -0.023" size="0.0015"/>
														  <site name="s14" pos="0.005 0 -0.012" size="0.0015"/>
														  <site name="s15" pos="0 0 0.014" size="0.0015"/>
														  <geom name="14_cylinder" type="cylinder" size="0.004 0.01" pos="-0.00575 0 0.01675" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
														  <geom name="15_cylinder" type="cylinder" size="0.01 0.01" pos="-0.007 0 0.032" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
														  <geom name="proximal_r" type="mesh" mesh="proximal_O" pos="-0.01 -0.008 0.045" euler="1.5707963249999999 3.1415926499999998 -2.617993875"/>
														  <site name="s16" pos="-0.014 0 0.021" size="0.0015"/>
														  <body name="distal_r" pos="-0.027 0 0.068" euler="0 1.1344640124999998 0">
															  <joint name="proximal_distal_r" type="hinge" axis="0 1 0" pos="0.041 0 0.0025" limited="true" range="-0.523598775 0.523598775" stiffness="1e-05" damping="1e-05"/>
															  <geom name="distal_r" type="mesh" mesh="distal_O" pos="-0.015 0.015 0.015" euler="-1.5707963249999999 1.5707963249999999 0"/>
															  <site name="s17" pos="0.022 0 0.009" size="0.0015"/>
														  </body>
													  </body>
												  </body>

												   <!-- Creating the left arm with its motor -->
												  <body name="Left Motor">
													  <site name="s21" pos="0.06 -0.025 0.035" size="0.0015"/>
													  <geom name="geom2" type="sphere" pos="0.06 -0.025 0.04" size="0.005"/>
													  <joint name="joint_2" type="hinge" pos="0.045 -0.025 0.04" axis="0 1 0" limited="true" range="-0.7853981624999999 0.7853981624999999" stiffness="1e-05" damping="1e-05"/>
												  </body>
												  <body name="swivel_l" pos="0.05 -0.025 0.0625" euler="0 0 -0.523598775">
													  <geom type="mesh" mesh="swivel_1"/>
													  <body name="proximal_l" pos="0.0038 0 0.0475">
														  <joint name="swivel_proximal_l" type="hinge" axis="0 1 0" pos="0.006 0 -0.03" limited="true" range="-0.7853981624999999 0.7853981624999999" stiffness="1e-05" damping="1e-05"/>
														  <site name="s22" pos="0.007 0 -0.04" size="0.0015"/>
														  <geom name="22_cylinder" type="cylinder" size="0.005 0.01" pos="0.005 0 -0.029" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
														  <site name="s231" pos="0.0035 0 -0.035" size="0.0015"/>
														  <site name="s23" pos="0 0 -0.03" size="0.0015"/>
														  <geom name="23_cylinder" type="cylinder" size="0.004 0.01" pos="0.0014 0 -0.0175" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
														  <site name="s232" pos="0.0035 0 -0.023" size="0.0015"/>
														  <site name="s24" pos="0.005 0 -0.012" size="0.0015"/>
														  <site name="s25" pos="0 0 0.014" size="0.0015"/>
														  <geom name="24_cylinder" type="cylinder" size="0.004 0.01" pos="-0.00575 0 0.01675" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
														  <geom name="25_cylinder" type="cylinder" size="0.01 0.01" pos="-0.007 0 0.032" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
														  <geom name="proximal_l" type="mesh" mesh="proximal_O" pos="-0.01 -0.008 0.045" euler="1.5707963249999999 3.1415926499999998 -2.617993875"/>
														  <site name="s26" pos="-0.014 0 0.021" size="0.0015"/>
														  <body name="distal_l" pos="-0.027 0 0.068" euler="0 1.1344640124999998 0">
															  <joint name="proximal_distal_l" type="hinge" axis="0 1 0" pos="0.041 0 0.0025" limited="true" range="-0.523598775 0.523598775" stiffness="1e-05" damping="1e-05"/>
															  <geom name="distal_l" type="mesh" mesh="distal_O" pos="-0.015 0.015 0.015" euler="-1.5707963249999999 1.5707963249999999 0"/>
															  <site name="s27" pos="0.022 0 0.009" size="0.0015"/>
														  </body>
													  </body>
												  </body>
										
												  <!-- Creating the center arm with its motor -->
												  <body name="Center Motor">
													  <site name="s31" pos="-0.03 0 0.035" size="0.0015"/>
													  <geom name="geom3" type="sphere" pos="-0.03 0 0.035" size="0.005"/>
													  <joint name="joint_3" type="hinge" pos="-0.045 0 0.035" axis="0 1 0" limited="true" range="-0.7853981624999999 0.7853981624999999" stiffness="1e-05" damping="1e-05"/>
												  </body>
												  <body name="proximal_c" pos="-0.0138 0 0.1105">
													  <joint name="swivel_proximal_c" type="hinge" axis="0 1 0" pos="-0.016 -0.01 -0.029" limited="true" range="-0.7853981624999999 0.7853981624999999" stiffness="1e-05" damping="1e-05"/>
													  <geom name="35_cylinder" type="cylinder" size="0.01 0.01" pos="-0.003 0 0.032" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
													  <geom name="proximal_c" type="mesh" mesh="proximal_O" pos="0 0.008 0.045" euler="1.5707963249999999 0 -2.617993875"/>
													  <site name="s32" pos="-0.016 0 -0.04" size="0.0015"/>
													  <geom name="32_cylinder" type="cylinder" size="0.005 0.01" pos="-0.018 0 -0.029" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
													  <site name="s331" pos="-0.0165 0 -0.035" size="0.0015"/>
													  <site name="s33" pos="-0.023 0 -0.03" size="0.0015"/>
													  <geom name="33_cylinder" type="cylinder" size="0.004 0.01" pos="-0.0115 0 -0.0175" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
													  <site name="s332" pos="-0.0165 0 -0.023" size="0.0015"/>
													  <site name="s34" pos="-0.018 0 -0.012" size="0.0015"/>
													  <site name="s35" pos="-0.012 0 0.014" size="0.0015"/>
													  <geom name="34_cylinder" type="cylinder" size="0.004 0.01" pos="-0.0045 0 0.01675" rgba=".3 .9 .3 .4" euler="1.5707963249999999 0 0"/>
													  <site name="s36" pos="0.0025 0 0.021" size="0.0015"/>
													  <body name="distal_c" pos="0.02 0 0.066" euler="0 2.0943951 0">
														  <joint name="proximal_distal_c" type="hinge" axis="0 1 0" pos="0.041 0 -0.0025" limited="true" range="-0.523598775 0.523598775" stiffness="1e-05" damping="1e-05"/>
														  <geom type="mesh" mesh="distal_O" pos="-0.015 -0.015 -0.015" euler="1.5707963249999999 1.5707963249999999 0"/>
														  <site name="s37" pos="0.022 0 -0.01" size="0.0015"/>
													  </body>
												  </body>
											  </body>





    										</body>
    									</body>
    								</body>
    								<body name="right_l4_2" pos="0 0 0">
    									<inertial diaginertia="1e-08 1e-08 1e-08" mass="1e-08" pos="1e-08 1e-08 1e-08" quat="0.820473 0.339851 -0.17592 0.424708"/>
    									<geom pos="0 0.01 0.26" size="0.06" name="right_l4_2"/>
    								</body>
    							</body>
    						</body>
    						<body name="right_l2_2" pos="0 0 0">
    							<inertial diaginertia="1e-08 1e-08 1e-08" mass="1e-08" pos="1e-08 1e-08 1e-08" quat="0.820473 0.339851 -0.17592 0.424708"/>
    							<geom pos="0 0 0.26" size="0.06" name="right_l2_2"/>
    						</body>
    					</body>
    					<body name="right_l1_2" pos="0 0 0">
    						<inertial diaginertia="1e-08 1e-08 1e-08" mass="1e-08" pos="1e-08 1e-08 1e-08" quat="0.820473 0.339851 -0.17592 0.424708"/>
    						<geom pos="0 0 0.035" size="0.07 0.07" type="cylinder" name="right_l1_2"/>
    					</body>
    				</body>
    			</body>
    		</body>
    	</body>
    	
        <body>
			<geom pos="0.9 0.15 -0.1" size="0.03 0.07" type="cylinder" name="target_body"/>
		</body>
    </worldbody>

	<tendon> <!-- Creating the tendon's path according to the sites -->
	  <spatial name="tendon_r" width="0.001 " rgba=".95 .3 .3 1" limited="true" range="0 {tendon_range}" stiffness="{tendon_stiffness}">
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
	  <spatial name="tendon_l" width="0.001 " rgba=".95 .3 .3 1" limited="true" range="0 {tendon_range}" stiffness="{tendon_stiffness}">
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
	  <spatial name="tendon_c" width="0.001 " rgba=".95 .3 .3 1" limited="true" range="0 {tendon_range}" stiffness="{tendon_stiffness}">
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

	<actuator>
	<motor ctrllimited="true" ctrlrange="-80.0 80.0" joint="right_j0" name="torq_right_j0"/>
	<motor ctrllimited="true" ctrlrange="-80.0 80.0" joint="right_j1" name="torq_right_j1"/>
	<motor ctrllimited="true" ctrlrange="-40.0 40.0" joint="right_j2" name="torq_right_j2"/>
	<motor ctrllimited="true" ctrlrange="-40.0 40.0" joint="right_j3" name="torq_right_j3"/>
	<motor ctrllimited="true" ctrlrange="-9.0 9.0" joint="right_j4" name="torq_right_j4"/>
	<motor ctrllimited="true" ctrlrange="-9.0 9.0" joint="right_j5" name="torq_right_j5"/>
	<motor ctrllimited="true" ctrlrange="-9.0 9.0" joint="right_j6" name="torq_right_j6"/>

	<!-- Right Finger Motors -->
	<motor joint="joint_1" name="swivel_proximal_r_motor" gear="1" ctrllimited="true" ctrlrange="{motor_lower_range} {motor_upper_range}"/>

	<motor joint="joint_2" name="swivel_proximal_l_motor" gear="1" ctrllimited="true" ctrlrange="{motor_lower_range} {motor_upper_range}"/>

	<motor joint="joint_3" name="swivel_proximal_c_motor" gear="1" ctrllimited="true" ctrlrange="{motor_lower_range} {motor_upper_range}"/>
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

</mujoco>
"""

with open("./assets/example_with_sawyer_with_object.xml", "w") as f:
    f.write(MODEL_XML)

f.close()