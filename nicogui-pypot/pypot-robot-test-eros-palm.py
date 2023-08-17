import json
import pypot
import pypot.robot

config_file = './nico_humanoid_upper_rh7d_ukba.json'

with open(config_file,'rt') as f:
    config = json.load(f)

alias = config['motorgroups']

MotorCls = pypot.dynamixel.motor.DxlSRBoard
motor = MotorCls(id=30,name='r_virtualhand_x',model='SR-EROSBRD',direct=True,offset=0,broken=False,angle_limit=[-180,180])
from pypot.dynamixel.io import DxlIO
dxl_io = DxlIO('COM6')
SyncLoopCls = getattr(pypot.dynamixel.syncloop, 'BaseDxlController')
controller = SyncLoopCls(dxl_io, [motor])
_robot = pypot.robot.Robot(motor_controllers=[controller], sync=True)

_robot.r_virtualhand_x.palm_sensor_reading

del _robot
