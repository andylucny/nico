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
    
def loadAnimation(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        concerned_dofs = eval(lines[0])
        recorded_poses = []
        for line in lines[1:]:
            recorded_pose = eval(line[:-1])
            recorded_poses.append(recorded_pose)
        return (concerned_dofs,recorded_poses)
    raise(BaseException(filename+" does not exist"))

dofs, poses = loadAnimation('movement.txt')
    
# enable torque
for dof in dofs:
    if dof != 'timestamp':
        robot.enableTorque(dof)

timeindex = np.where(np.array(dofs) == 'timestamp')[0][0]
timestamps = []
for pose in poses:
    timestamps.append(pose[timeindex])

timestamps = np.array(timestamps,np.float64)/1000.0 #[s]
durations = [timestamps[0]] + list(timestamps[1:]-timestamps[:-1])

def move_to_position_through_time(target_positions, duration):
    if duration == 0:
        return
    global robot
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

def play_movement(dofs,poses,durations):
    for pose,duration in zip(poses,durations):
        # Move all joints in the subset to the postion
        command = {dof : angle for dof, angle in zip(dofs, pose) if dof != 'timestamp' }
        move_to_position_through_time(command, duration)
        time.sleep(duration)

command0 = {dof : angle for dof, angle in zip(dofs, poses[0]) if dof != 'timestamp' }
move_to_position_through_time(command0,2)

for _ in range(4):
    play_movement(dofs,poses,durations)
    durations = [ duration * 2 for duration in durations ]
    time.sleep(1)

