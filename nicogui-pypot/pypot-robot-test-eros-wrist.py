import json
import pypot
import pypot.robot

config_file = './nico_humanoid_upper_rh7d_ukba.json'

with open(config_file,'rt') as f:
    config = json.load(f)

MotorCls = pypot.dynamixel.motor.DxlSRErosMotor
motor = MotorCls(id=31,name='r_wrist_z',model='SR-SEED28',direct=True,offset=0,broken=False,angle_limit=[-180,180])

from pypot.dynamixel.io import DxlIO
dxl_io = DxlIO('COM6')

old_limits = dxl_io.get_angle_limit((motor.id, ))[0]
old_return_delay_time = dxl_io.get_return_delay_time((motor.id, ))[0]
dxl_io.set_angle_limit({31:(-180,180)})
dxl_io.set_return_delay_time({31:0})

SyncLoopCls = getattr(pypot.dynamixel.syncloop, 'BaseDxlController')
controller = SyncLoopCls(dxl_io, [motor])
_robot = pypot.robot.Robot(motor_controllers=[controller], sync=True)

_robot.r_wrist_z.goto_position(0,1)

del _robot
