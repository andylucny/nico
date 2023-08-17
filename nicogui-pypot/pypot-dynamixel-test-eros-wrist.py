from pypot.dynamixel.io import DxlIO
dxl_io = DxlIO('COM6')
dxl_io.enable_torque([1,5,31])
dxl_io.set_moving_speed({1:50,5:50,31:50})
dxl_io.set_goal_position({1:0,5:-70})
dxl_io.get_goal_position([31])
dxl_io.set_goal_position({31:-100})
del dxl_io

