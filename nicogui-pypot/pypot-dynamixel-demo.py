from pypot.dynamixel.io import DxlIO
dxl_io = DxlIO('/dev/ttyUSB0')
motor_IDs = dxl_io.scan()
num_motors = len(motor_IDs)
print("Found", num_motors, "motors with current angles",  dxl_io.get_present_position(motor_IDs))
dxl_io.set_goal_position(dict(zip(motor_IDs, num_motors*[0])))

dxl_io.enable_torque(motor_IDs)
speed = dict(zip(motor_IDs,[200 for _ in motor_IDs])) #40
dxl_io.set_moving_speed(speed)
dxl_io.set_goal_position({2:0,6:70})
dxl_io.get_goal_position([41])
dxl_io.set_goal_position({41:-180})
dxl_io.set_goal_position({41:0})
dxl_io.disable_torque([41])
dxl_io.set_goal_position({1:0,5:-70})
dxl_io.get_goal_position([31])
dxl_io.set_goal_position({31:100})

del dxl_io
