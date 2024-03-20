import time
import numpy as np

from ikpy.chain import Chain
my_chain = Chain.from_urdf_file("nico_right_arm.urdf")

from nicomotion.Motion import Motion
motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
robot = Motion(motorConfig=motorConfig)

rightArmDofs = ['r_shoulder_z','r_shoulder_y','r_arm_x','r_elbow_y']
for dof in rightArmDofs:
    robot.disableTorque(dof)
    
def rad(x):
    return np.pi*x/180.0

while True:
    angles = [ 0 ]
    for dof in rightArmDofs:
        angle = robot.getAngle(dof)
        angles.append(rad(angle))
    angles += [ 0, 0, 0 ]
    point = my_chain.forward_kinematics(angles)[:3, 3]
    print(point)
    time.sleep(1)

