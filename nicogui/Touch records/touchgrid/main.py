from nicomotors import NicoMotors
from time import sleep

motors = NicoMotors()
motors.open()
leftArmDofs = ['left-arm1', 'left-arm2', 'left-arm3', 'left-elbow1', 'left-wrist1', 'left-wrist2', 'left-thumb1', 'left-thumb2', 'left-forefinger', 'left-littlefingers', 'neck1', 'neck2']

for dof in leftArmDofs:
	motors.enableTorque(dof)

def setLeftArm(angles):
	for dof,angle in zip(leftArmDofs,angles):
		motors.setPositionDg(dof,angle)

angles = [-9.0, 48.0, 1.0, 77.0, 58.0, 16.0, 0.0, 32.0, 0.0, 20.0, -2.0, 0.0]
setLeftArm(angles)

def touch(p):
	print(ord(p[0])-ord('A'), ord(p[1])-ord('1'))
	pass

touch('A1')

