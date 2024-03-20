import time
import numpy as np

from ikpy.chain import Chain
my_chain = Chain.from_urdf_file("nico_right_arm.urdf")

from nicomotion.Motion import Motion
motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
robot = Motion(motorConfig=motorConfig)

rightArmDofs = ['r_shoulder_z','r_shoulder_y','r_arm_x','r_elbow_y']
for dof in rightArmDofs:
    robot.enableTorque(dof)
    
point = [ 0.3371747,  -0.25679694,  0.24113979]

rad_angles = my_chain.inverse_kinematics(point)

def deg(x):
    return 180.0*x/np.pi

def rad(x):
    return np.pi*x/180.0
    
angles = [ deg(rad_angle) for rad_angle in rad_angles ]
print(angles[1:5])

expected_angles = [0, -0.3045599544730105, 0.9183922523994161, 0.02076941809873252, 2.199463923363254, 0, 0, 0 ]
print([ deg(expected_angle) for expected_angle in expected_angles[1:5] ])

angular_speed = 0.04
for dof, angle in zip(rightArmDofs,angles[1:5]):
    robot.setAngle(dof, angle, angular_speed)

time.sleep(2)

measured_angles = [ 0 ]
for dof in rightArmDofs:
    measured_angle = robot.getAngle(dof)
    measured_angles.append(rad(measured_angle))

measured_angles += [ 0, 0, 0 ]

print(measured_angles[1:5])
