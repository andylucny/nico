from nicomotion.Motion import Motion
import time
import numpy as np
motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
robot = Motion(motorConfig=motorConfig)

import os
def quit():
    global robot
    del robot
    os._exit(0)
    
dofs = [ 'r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x', 'r_thumb_z', 'r_thumb_x', 'r_indexfinger_x', 'r_middlefingers_x' ]

# enable torque
for dof in dofs:
    robot.enableTorque(dof)

# set PIDs
#for dof in dofs[:4]:
#    robot.setPID(dof,32,3,0.5)
#    time.sleep(0.1)

pose0 = [-11.0, -6.0, 32.0, 64.0, 72.0, 145.0, -61.0, 21.0, -180.0, 171.0]
defaultSpeed = 0.02
#for dof, angle in zip(dofs,pose0):
#    robot.setAngle(dof,angle,defaultSpeed)

#print(robot.getPID('r_arm_x'))
#robot.setPID('r_arm_x',32,3,3)

poses = np.array([
    [ -11.,   -6.,   32.,   64.,   72.,  145.,  -61.,   21., -180., 171.],
    [  21.,   -4.,   67.,   87.,   -2.,  145.,  -61.,   21., -180., 171.],
    [  41.,    1.,   70.,  108.,  -27.,  145.,  -61.,   21., -180., 171.],
    [  52.,    5.,   70.,  118.,  -32.,  145.,  -61.,   21., -180., 171.],
    [  59.,    5.,   70.,  120.,  -44.,  145.,  -61.,   21., -180., 171.]
],np.float32)

timestamps = np.array([ 0., 160., 220., 250., 290. ],np.float32)/100.0 #[s]

def move_position(target_positions, speed, real=True):
    global robot, dofs
    # calculate current angular speed
    cur_speed = (63.0 / 60) * 360 * speed / 0.3
    import copy
    # get the current positions of all joints to move
    current_positions = copy.deepcopy(target_positions)
    for joint in current_positions:
        current_positions[joint] = robot.getAngle(joint)
    time_to_reach = {
        k: abs(
            (float(current_positions[k]) - float(target_positions[k])) / cur_speed
        )
        for k in current_positions
    }
    # print time_to_reach
    max_time = max(list(time_to_reach.values())[:4])
    max_keys = [k for k, v in time_to_reach.items() if v == max_time]
    print("Max time: " + str((max_keys, max_time)))
    for joi in target_positions:
        if real and max_time != 0.0:
            robot.setAngle(
                joi,
                float(target_positions[joi]),
                ((speed * time_to_reach[joi]) / max_time),
            )
    return max_time

command0 = dict(zip(dofs,pose0))
#duration = move_position(command0,defaultSpeed)
#time.sleep(duration)

pose1 = poses[1]
command1 = dict(zip(dofs,pose1))
#duration = move_position(command1,defaultSpeed)
#time.sleep(duration)

pose2 = poses[2]
command2 = dict(zip(dofs,pose2))
#duration = move_position(command2,defaultSpeed)
#time.sleep(duration)

def play_movement(poses,move_speed):
    for pose in poses:
        # Move all joints in the subset to the postion
        command = {k: pose[k] for k in pose}
        mt = move_position(command, move_speed)
        time.sleep(mt)
    
play_movement([command0,command1,command2],defaultSpeed)

