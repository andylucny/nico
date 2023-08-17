import json
import pypot
import pypot.robot

config_file = './nico_humanoid_upper_rh7d_ukba.json'

with open(config_file,'rt') as f:
    config = json.load(f)

_robot = pypot.robot.from_config(config)

_robot.motors[0].compliant = False # torque on
_robot.motors[0].goto_position(0, duration=2, wait=False) #2s

_robot.r_shoulder_y.compliant = False
_robot.r_elbow_y.compliant = False
_robot.r_elbow_y.goto_position(-65, duration=1, wait=False) 

_robot.r_wrist_z.compliant = False
_robot.r_wrist_z.moving_speed = 50
_robot.r_wrist_z.goal_position = 0

_robot.r_virtualhand_x.palm_sensor_reading
#

_robot.r_wrist_z.compliant = False
_robot.r_wrist_z.goto_position(180, duration=3, wait=False) 

#--- 

_robot.r_elbow_y.compliant = False
_robot.r_elbow_y.position = 100

_robot.r_wrist_z.compliant = False
_robot.r_wrist_z.position = 100

state = dict()
for motor in _robot.motors:
    state[motor.name] = motor.present_position

#for motor in _robot.motors:
#    if hasattr(motor, "force_control_enable"):
#        motor.force_control_enable = True # False
#        motor.goal_force = goalForce

speed = 0.05
angle = 90
jointName = 'r_wrist_z'
for motor in _robot.motors:
    motor = getattr(_robot, jointName)
    motor.compliant = False
    motor.goal_speed = 1000.0 * speed
    motor.goal_position = angle

