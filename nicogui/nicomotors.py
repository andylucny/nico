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

    joints = {  # 'key'       : [ DXL_ID, [dg0,bin0,coef] dg=dg0+coef*(bin-bin0), [bin-from,bin-default,bin-to], [(dg,bin,name)], [MinDg, MaxDg, MinDg, MaxDg, Inverted] ]
        'left-arm1'           : [ 22, [0,2060,-0.0865],  [2153,2060,1029], [(-10,2155,'forward'),(0,2060,'sideway'),(90,1010,'backward')], [  -75,  55, -100, 125, False] ],
        'left-arm2'           : [  2, [0,2080,-0.0865],  [ 615,2080,2281], [(-20,2281,'behind'),(0,2080,'down'),(90,1020,'forward'),(135,600,'raise')], [  -30, 100, -180, 179, False] ],
        'left-arm3'           : [  4, [0,1550,0.0865],   [1219,1982,1982], [(-45,1000,'up-sideway'),(0,1550,'straight'),(45,2020,'down-attach')], [ -118,  87, -140, 100, True ] ],
        'left-elbow1'         : [  6, [180,2030,-0.0865],[3169,3070,2030], [(52,3500,'closed'),(90,3070,'right-angled'),(180,2030,'straight')], [ -100,   0, -100, 180, False] ],
        'left-wrist1'         : [ 41, [-90,0,0.045],     [   0,2000,4000], [(-90,0,'palm-up'),(0,2000,'palm-vertical'),(90,4000,'palm-vertical')], [  -80,  80, -180, 180, True ] ],
        'left-wrist2'         : [ 43, [0,1300,-0.0285],  [   0,1300,4095], [(-40,0,'opened'),(0,1300,'straight'),(75,4095,'closed')], [    0,  50, -180, 180, False] ],
        'left-thumb1'         : [ 45, [0,0,0.043956],    [   0,   0,4095], [(0,0,'opened'),(180,4095,'closed')],[  -75,   0, -180, 180, True ] ],
        'left-thumb2'         : [ 44, [0,0,0.043956],    [   0,   0,4095], [(0,0,'opened'),(180,4095,'closed')],[  -75,   0, -180, 180, True ] ],
        'left-forefinger'     : [ 46, [0,0,0.043956],    [   0,   0,4095], [(0,0,'opened'),(180,4095,'closed')],[  -75,   0, -180, 180, True ] ],
        'left-littlefingers'  : [ 47, [0,0,0.043956],    [   0,   0,4095], [(0,0,'opened'),(180,4095,'closed')],[  -75,   0,    0,   0, False] ],
        'right-arm1'          : [ 21, [0,2060,0.0865],   [1804,2060,3045], [(-10,1800,'forward'),(0,2060,'sideway'),(90,3070,'backward')], [  -75,  55, -100, 125, False] ],
        'right-arm2'          : [  1, [0,2050,0.0865],   [1820,2050,3444], [(-20,1810,'behind'),(0,2050,'down'),(90,3040,'forward'),(135,3460,'raise')], [  -30, 100, -180, 179, False] ],
        'right-arm3'          : [  3, [0,2460,-0.0865],  [2052,2052,2880], [(-45,3140,'up-sideway'),(0,2460,'straight'),(45,2050,'down-attach')], [ -118,  87, -140, 100, True ] ],
        'right-elbow1'        : [  5, [180,2030,0.0865], [ 905,1040,2030], [(52,550,'closed'),(90,1040,'right-angled'),(180,2030,'straight')], [ -100,   0, -100, 180, False] ],
        'right-wrist1'        : [ 31, [90,0,-0.045],     [   0,2000,4000], [(-90,4000,'palm-up'),(0,2000,'palm-vertical'),(90,0,'palm-vertical')], [  -80,  80, -180, 180, True ] ],
        'right-wrist2'        : [ 33, [0,1300,0.0285],   [   0,1300,4095], [(-40,0,'opened'),(0,1300,'straight'),(75,4095,'closed')], [    0,  50, -180, 180, False] ],
        'right-thumb1'        : [ 35, [0,0,0.043956],    [   0,   0,4095], [(0,0,'opened'),(180,4095,'closed')],[  -75,   0, -180, 180, True ] ],
        'right-thumb2'        : [ 34, [0,0,0.043956],    [   0,   0,4095], [(0,0,'opened'),(180,4095,'closed')],[  -75,   0, -180, 180, True ] ],
        'right-forefinger'    : [ 36, [0,0,0.043956],    [   0,   0,4095], [(0,0,'opened'),(180,4095,'closed')], [  -75,   0, -180, 180, True ] ],
        'right-littlefingers' : [ 37, [0,0,0.043956],    [   0,   0,4095], [(0,0,'opened'),(180,4095,'closed')],[  -75,   0, -180, 180, False] ],
        'neck1'               : [ 20, [0,2070,0.08125],  [1592,2070,2397], [(-30,1590,'forward-bend'),(0,2070,'upright'),(20,2400,'backward-bend')], [    0,  50, -180, 180, False] ],
        'neck2'               : [ 19, [0,2095,-0.09278], [1614,2095,2571], [(-45,2580,'to-left'),(0,2095,'forward'),(45,1610,'to-right')], [   -90, 90, -180, 180, False] ],
    }
    
    # Control table address
    ADDR_MX_TORQUE_ENABLE       = 24 
    ADDR_MX_GOAL_POSITION       = 30
    ADDR_MX_MOVING_SPEED        = 32
    ADDR_MX_PRESENT_POSITION    = 36
    
    # Values
    TORQUE_ENABLE               = 1                             # Value for enabling the torque
    TORQUE_DISABLE              = 0                             # Value for disabling the torque
    DEFAULT_MOVING_SPEED        = 40

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

    def bin2dg(self, k, bin):
        dg0, bin0, coef = self.joints[k][1]
        dg = dg0 + coef*(bin-bin0)
        return dg

    def dg2bin(self, k, dg):
        dg0, bin0, coef = self.joints[k][1]
        bin = bin0 + (dg-dg0)/coef
        return bin

    def getRange(self, k):
        vals = self.joints[k][2]
        minv = np.min(vals)
        maxv = np.max(vals)
        defv = np.median(vals)
        return minv, maxv, defv

    def getRangeDg(self, k):
        vals = [self.bin2dg(k,v) for v in self.getRange(k)]
        minv = np.min(vals)
        maxv = np.max(vals)
        defv = np.median(vals)
        return minv, maxv, defv

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
        # set default moving speed
        for k in self.keys:
            self.setMovingSpeed(k)

    def enableTorque(self,k): # Enable Dynamixel Torque
        if self.opened:
            id = self.joints[k][0]
            errno, result = self.handler.write1ByteTxRx(port=self.port, dxl_id=id, address=self.ADDR_MX_TORQUE_ENABLE, data=self.TORQUE_ENABLE)

    def disableTorque(self,k): # Disable Dynamixel Torque
        if self.opened:
            id = self.joints[k][0]
            errno, result = self.handler.write1ByteTxRx(port=self.port, dxl_id=id, address=self.ADDR_MX_TORQUE_ENABLE, data=self.TORQUE_DISABLE)
            
    def getDefaultPosition(self,k):
        return self.joints[k][2][1]

    def getDefaultPositionDg(self,k):
        return self.bin2dg(k,self.getDefaultPosition(k))
        
    def getPosition(self,k): # Read actual position
        if self.opened:
            id = self.joints[k][0]
            position, errno, result = self.handler.read2ByteTxRx(port=self.port, dxl_id=id, address=self.ADDR_MX_PRESENT_POSITION)
            return position
        else:
            return self.getDefaultPosition(k)
            
    def getPositionDg(self,k):
        return self.bin2dg(k,self.getPosition(k))
    
    def setPosition(self,k,position):
        if self.opened:
            id = self.joints[k][0]
            errno, result = self.handler.write2ByteTxRx(port=self.port, dxl_id=id, address=self.ADDR_MX_GOAL_POSITION, data=position)
    
    def setPositionDg(self,k,positionDg):
        self.setPosition(k,self.dg2bin(positionDg))

    def setMovingSpeed(self,k,speed=DEFAULT_MOVING_SPEED):
        if self.opened:
            id = self.joints[k][0]
            errno, result = self.handler.write2ByteTxRx(port=self.port, dxl_id=id, address=self.ADDR_MX_MOVING_SPEED, data=speed)

    def close():
        if self.opened:
            self.port.closePort()
            self.opened = False
