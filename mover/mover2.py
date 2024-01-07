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
#    robot.setPID(dof,32.0,3.0,0.5)
#    time.sleep(0.1)

poses = np.array([
    [ -11.,   -6.,   32.,   64.,   72.,  145.,  -61.,   21., -180., 171.],
    [  21.,   -4.,   67.,   87.,   -2.,  145.,  -61.,   21., -180., 171.],
    [  41.,    1.,   70.,  108.,  -27.,  145.,  -61.,   21., -180., 171.],
    [  52.,    5.,   70.,  118.,  -32.,  145.,  -61.,   21., -180., 171.],
    [  59.,    5.,   70.,  120.,  -44.,  145.,  -61.,   21., -180., 171.]
],np.float32)

timestamps = np.array([ 0., 160., 220., 250., 290. ],np.float64)/100.0 #[s]
durations = [1.5] + list(timestamps[1:]-timestamps[:-1])

def move_to_position_through_time(target_positions, duration):
    global robot, dofs
    # calculate current angular speed
    import copy
    # get the current positions of all joints to move
    current_positions = copy.deepcopy(target_positions)
    for joint in current_positions:
        current_positions[joint] = robot.getAngle(joint)
    speed_to_reach = {
        k: abs(
            (float(current_positions[k]) - float(target_positions[k])) / float(1260*duration)
        )
        for k in current_positions
    }
    for joi in target_positions:
        robot.setAngle(
            joi,
            float(target_positions[joi]),
            speed_to_reach[joi],
        )

pose0 = poses[0]
command0 = dict(zip(dofs,pose0))
pose1 = poses[1]
command1 = dict(zip(dofs,pose1))
pose2 = poses[2]
command2 = dict(zip(dofs,pose2))

def play_movement(poses,durations):
    for pose,duration in zip(poses,durations):
        # Move all joints in the subset to the postion
        command = {k: pose[k] for k in pose}
        move_to_position_through_time(command, duration)
        time.sleep(duration)
    
play_movement([command0,command1,command2],durations[:3])

move_to_position_through_time(command0,2)

#uvazovat zrychlovanie nahratej trajektorie
