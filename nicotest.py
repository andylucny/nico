import time

from nicomotion import Motion
from os.path import dirname, abspath

robot = Motion.Motion(nico_root + "/json/nico_humanoid_upper.json", vrep=False)
robot.setAngle("r_arm_x", -60, 0.05)
robot.setAngle("r_elbow_y", -20, 0.05)