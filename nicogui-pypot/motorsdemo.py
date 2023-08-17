from nicomotion.Motion import Motion
motorConfig = './nico_humanoid_upper_rh7d_ukba.json'
robot = Motion(motorConfig=motorConfig)
robot.enableTorqueAll()
robot.enableTorque("head_z")
robot.setAngle("head_z", 0, 0.05) # joint[name], angle[dg], speed
robot.getAngle("head_z") # joint[name]; return angle[dg]
robot.changeAngle("head_y", 0, 0.05) # joint[name], angle[dg], speed
robot.disableTorqueAll()
robot.disableTorque("head_z")
robot.disableForceControl("head_z")
robot.enableForceControl("head_z")
robot.disableForceControlAll()
robot.enableForceControlAll()
robot.getAngleLowerLimit("head_z") # joint[name]; return angle[dg]
robot.getAngleUpperLimit("head_z") # joint[name]; return angle[dg]
robot.getJointNames() # list of joint[name]s  
robot.getPalmSensorReading("r_hand") # or l_hand  touch<=15
robot.getPose(objectName, relativeToObject=None) # returns x,y,z not working: 'Robot' object has no attribute 'get_object_position'
robot.getSpeed(jointName)
handName='r_hand'
robot.openHand(handName, fractionMaxSpeed=1.0, percentage=1.0)
poseName = "thumbsUp"
#poseName = "pointAt"
robot.setHandPose(handName, poseName, fractionMaxSpeed=1.0, percentage=1) # do nothing
# poseName: "thumbsUp", "pointAt", "okSign", "pinchToIndex", "keyGrip", "pencilGrip", "closeHand", "openHand"
robot.setMaximumSpeed(maximumSpeed) # 0 <= maximumSpeed <= 1.0
robot.toSafePosition() # before disable torque
robot.getAngleLowerLimit('l_elbow_y')
robot.setAngle('l_elbow_y',,0.05)
del robot # close

speed 0.05
head_z - head from right(-90) through straight(0) to left(90)
head_y - head from top(25) through straight() to bottom(-40)

l_shoulder_z -v +0 25 dozadu, 0 do strany, -80 dopredu
l_shoulder_y -v +0 30 vzad 0 dolu, -90 dopredu, -180 hore
l_arm_x -v -5 max k telu, 0 dolu, 90 doboku, 110 max hore
l_elbow_y 135.74-v:  -43.3 .. 180 rovno, 44.53 .. 90 pravy uhol, 82 .. k telu

r_shoulder_z v -25 dozadu, 0 do strany, 80 dopredu
r_shoulder_y v -30 vzad 0 dolu, 90 dopredu, 180 hore
r_arm_x v  5 max k telu, 0 dolu, -90 doboku, -110 max hore
r_elbow_y v+135.74 44.26 .. 180 rovno, -46.64 .. 90 pravy uhol, -86.64 ..49 k ramenu

r_wrist_z -v/2 -180 .. -90 palec dnu, 0..palec hore, +180 .. 90 palec von
r_wrist_x -v/4 180 .. -45 plne zavreta, 0 rovno, -180 plne otvorena .. 45
r_thumb_z 
r_thumb_x
r_indexfinger_x
r_middlefingers_x
ziadne z tychto neovlada ked je pritomna virtual hand

l_wrist_z 
l_wrist_x
l_thumb_z
l_thumb_x
l_indexfinger_x
l_middlefingers_x

import time
joint = 'r_wrist_z'
print(robot.getAngleLowerLimit(joint),'-',robot.getAngleUpperLimit(joint))
for i in range(200):
    print(robot.getAngle(joint))
    time.sleep(0.5)

robot.setAngle('r_wrist_z',0,0.05)