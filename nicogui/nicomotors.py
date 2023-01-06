import os, sys
import time
import numpy as np

import dynamixel_sdk as dynamixel   

class NicoMotors:

#right_hand_motor_indexes = [0, 16, 12, 14, 18, 10, 8, 3]
#right_hand_motor_DXL_IDs = [47, 21,  1,  3,  5, 31, 33, 36]
#min_motor_angles = [0, -100, -180, -140, -100, -180, -180, -180, 180, -180]
#max_motor_angles = [0, 125, 179, 75, 100, 180, 180, 180, 180, 180, 180]
#inverted_motors = [False, False, False, True, False, True, False, True, True, True]
#0, -75,  -30, -118, -100, -80,  0, -75, -75, -75
#0,  55,  100,   87,    0,  80, 50,   0,   0,   0

    joints = {  # 'key'       : [ DXL_ID, MinDg, MaxDg, Inverted ]
        'left-arm1'           : [ 22,  -75,  55, -100, 125, False  ],
        'left-arm2'           : [  2,  -30, 100, -180, 179, False  ],
        'left-arm3'           : [  4, -118,  87, -140, 100, True   ],
        'left-elbow1'         : [  6, -100,   0, -100, 180, False  ],
        'left-wrist1'         : [ 41,  -80,  80, -180, 180, True   ],
        'left-wrist2'         : [ 43,    0,  50, -180, 180, False  ],
        'left-thumb1'         : [ 45,  -75,   0, -180, 180, True   ],
        'left-thumb2'         : [ 44,  -75,   0, -180, 180, True   ],
        'left-forefinger'     : [ 46,  -75,   0, -180, 180, True   ],
        'left-littlefingers'  : [ 47,  -75,   0,    0,   0, False  ],
        'right-arm1'          : [ 21,  -75,  55, -100, 125, False ],
        'right-arm2'          : [  1,  -30, 100, -180, 179, False ],
        'right-arm3'          : [  3, -118,  87, -140, 100, True  ],
        'right-elbow1'        : [  5, -100,   0, -100, 180, False ],
        'right-wrist1'        : [ 31,  -80,  80, -180, 180, True  ],
        'right-wrist2'        : [ 33,    0,  50, -180, 180, False ],
        'right-thumb1'        : [ 35,  -75,   0, -180, 180, True  ],
        'right-thumb2'        : [ 34,  -75,   0, -180, 180, True  ],
        'right-forefinger'    : [ 36,  -75,   0, -180, 180, True  ],
        'right-littlefingers' : [ 37,  -75,   0, -180, 180, False ],
        'neck1'               : [ 20,    0,  50, -180, 180, False ],
        'neck2'               : [ 19,   -90, 90, -180, 180, False ],
    }
    
    # Control table address
    ADDR_MX_TORQUE_ENABLE       = 24 
    ADDR_MX_GOAL_POSITION       = 30
    ADDR_MX_PRESENT_POSITION    = 36
    
    # Values
    TORQUE_ENABLE               = 1                             # Value for enabling the torque
    TORQUE_DISABLE              = 0                             # Value for disabling the torque

    # Protocol version
    PROTOCOL_VERSION            = 1
    
    # Baud rate
    BAUDRATE                    = 1000000

    def __init__(self, portname):
        self.portname = portname
        self.keys = [key for key in self.joints.keys()]
        self.opened = False
        
    def dofs(self):
        return self.keys

    def range(self, k):
        v = self.joints[k]
        #return k, v[1], v[2], (v[1]+v[2])//2
        return 0, 4095, 2048

    def open(self):
        self.port = dynamixel.PortHandler(self.portname)
        if self.port.openPort():
            print("Succeeded to open the port",self.portname)
        else:
            print("Failed to open the port",self.portname)
            os._exit(1)
        if self.port.setBaudRate(self.BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            os._exit(1)
        self.handler = dynamixel.PacketHandler(protocol_version=self.PROTOCOL_VERSION)
        self.opened = True

    def enableTorque(self,k): # Enable Dynamixel Torque
        if self.opened:
            id = self.joints[k][0]
            errno, result = self.handler.write1ByteTxRx(port=self.port, dxl_id=id, address=self.ADDR_MX_TORQUE_ENABLE, data=self.TORQUE_ENABLE)

    def disableTorque(self,k): # Disable Dynamixel Torque
        if self.opened:
            id = self.joints[k][0]
            errno, result = self.handler.write1ByteTxRx(port=self.port, dxl_id=id, address=self.ADDR_MX_TORQUE_ENABLE, data=self.TORQUE_DISABLE)

    def getPosition(self,k): # Read actual position
        if self.opened:
            id = self.joints[k][0]
            position, errno, result = self.handler.read2ByteTxRx(port=self.port, dxl_id=id, address=self.ADDR_MX_PRESENT_POSITION)
            return position
    
    def setPosition(self,k,position):
        if self.opened:
            id = self.joints[k][0]
            errno, result = self.handler.write2ByteTxRx(port=self.port, dxl_id=id, address=self.ADDR_MX_GOAL_POSITION, data=position)
        
    def close():
        if self.opened:
            self.port.closePort()
            self.opened = False
