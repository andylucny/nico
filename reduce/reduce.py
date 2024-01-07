import numpy as np

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

dofs, anim = loadAnimation('2.txt')
anim = np.array([ pose + [t*10] for t,pose in enumerate(anim)]) # 10ms period

import numpy as np

def distance_point_to_line(point, start, end):
    """
    Calculate the perpendicular distance from a point to a line defined by two other points.
    This version works for N-dimensional space.
    """
    if np.all(start == end):
        return np.linalg.norm(point - start)
    
    line_vector = end - start
    point_vector = point - start
    projection = np.dot(point_vector, line_vector) / np.dot(line_vector, line_vector)
    if 0 <= projection <= 1:
        perpendicular = point_vector - projection * line_vector
        return np.linalg.norm(perpendicular)
    else:
        # If the projection is outside the segment, use the distance to the closest endpoint
        return min(np.linalg.norm(point - start), np.linalg.norm(point - end))

def rdp_simplify(points, epsilon=2.0):
    """
    Simplify a trajectory using the Ramer-Douglas-Peucker algorithm.
    """
    if len(points) <= 2:
        return points

    # Find the point with the maximum distance
    d_max = 0
    index = 0
    start, end = points[0][:-1], points[-1][:-1]

    for i in range(1, len(points) - 1):
        d = distance_point_to_line(points[i][:-1], start, end)
        if d > d_max:
            index = i
            d_max = d

    # If the maximum distance is greater than the threshold, recursively simplify both segments
    if d_max > epsilon:
        recursive1 = rdp_simplify(points[:index + 1], epsilon)
        recursive2 = rdp_simplify(points[index:], epsilon)

        # Concatenate the results
        result = np.vstack((recursive1[:-1], recursive2))
    else:
        # Otherwise, the current segment is within the accuracy threshold
        result = np.vstack((points[0], points[-1]))

    return result

# Set the desired accuracy (adjust as needed)
epsilon = 4.0
simplified_anim = rdp_simplify(anim, epsilon)
print(len(simplified_anim))

"""
from nicomotion.Motion import Motion
import time
motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
robot = Motion(motorConfig=motorConfig)

import os
def quit():
    global robot
    del robot
    os._exit(0)

# enable torque
def enable():
    for dof in dofs:
        robot.enableTorque(dof)

enable()

# replay
def replay(dofs, anim):
    defaultSpeed = 0.04*0.5
    for pose in anim:
        for dof, angle in zip(dofs, pose[:-1]):
            robot.setAngle(dof,angle,defaultSpeed)
        time.sleep(pose[-1]/1000.0)

#replay(dofs,anim[:1])
#replay(dofs,anim)
#replay(dofs,anim[:1])
#replay(dofs,simplified_anim)

def replay(dofs, anim):
    defaultSpeed = 0.04*0.5
    for i, pose in enumerate(anim):
        duration = (pose[-1]-anim[i-1][-1])/1000.0 if i > 0 else 0.01
        print(duration)
        for dof, angle in zip(dofs, pose[:-1]):
            robot.setAngle(dof,angle,defaultSpeed)
        time.sleep(duration)

def replay2(dofs, anim):
    for i, pose in enumerate(anim):
        duration = (pose[-1]-anim[i-1][-1])/1000.0 if i > 0 else 0.01
        print(duration)
        for dof, angle in zip(dofs, pose[:-1]):
            motor = getattr(robot._robot, dof)
            motor.goto_position(angle,duration=duration, wait=False) 
        time.sleep(duration*10)

#replay2(dofs,anim[:1])
#replay2(dofs,anim)
#replay2(dofs,anim[:1])
#replay2(dofs,simplified_anim)
"""
