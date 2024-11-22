import numpy as np
np.set_printoptions(precision=3,suppress=True)
import matplotlib.pyplot as plt
from pprint import pprint
import cv2

def rad(value):
    return value * np.pi/180.0

def Txyz(tx,ty,tz):
    return np.array([
        [ 1, 0, 0, tx ],
        [ 0, 1, 0, ty ],
        [ 0, 0, 1, tz ],
        [ 0, 0, 0, 1 ],
    ])
  
def Rz(theta):
    theta = rad(theta)
    return np.array([
        [ np.cos(theta), -np.sin(theta), 0, 0 ],
        [ np.sin(theta),  np.cos(theta), 0, 0 ],
        [             0,              0, 1, 0 ],
        [             0,              0, 0, 1 ],
    ])
   
def Rx(alpha):
    alpha = rad(alpha)
    return np.array([
        [ 1,             0,              0, 0 ],
        [ 0, np.cos(alpha), -np.sin(alpha), 0 ],
        [ 0, np.sin(alpha),  np.cos(alpha), 0 ],
        [ 0,             0,              0, 1 ],
    ])

def Ry(beta):
    beta = rad(beta)
    return np.array([
        [  np.cos(beta), 0,   np.sin(beta), 0 ],
        [             0, 1,              0, 0 ],
        [ -np.sin(beta), 0,   np.cos(beta), 0 ],
        [             0, 0,              0, 1 ],
    ])

def Ts(thetas):
    return [
        Txyz(0,5,19.5), Rz(90), Rz(thetas[0]), # -> 'r_shoulder_z'
        Txyz(0,-1.5,2.5), Ry(90), Rz(thetas[1]), # -> 'r_shoulder_y'
        Txyz(3,0,9.5), Rx(-90), Rz(-thetas[2]), # -> 'r_arm_x'
        Txyz(17.5,0,0), Rx(90), Rz(180), Rz(-thetas[3]), # -> 'r_elbow_y'
        Txyz(10,0,0), Ry(90), Rz(-thetas[4]/2.0), # -> 'r_wrist_z'
        Txyz(0,0,10), Rx(-90), Rz(-90), Rz(thetas[5]/4.5), # -> 'r_wrist_x'
        Txyz(0,0,2), Txyz(10,0,0), Txyz(0,-2.5,0), Ry(90), Rz(90)
    ]

def dk(thetas):
    point0 = np.array([[0,0,0,1]]).T
    e = np.eye(4)
    points = [ point0.T[0][:3] ]
    re = e
    for T in Ts(thetas):
        re = re @ T
        points.append( (re @ point0).T[0][:3] )

    return points
    
if __name__ == '__main__':
        
    carlo_matilde = [-25.0, 83.0, 47.0, 94.0, -59.0, 114.0]
    points0 = dk(carlo_matilde)
    print(points0[-1]) # [-6.53  31.56  50.163]

    touch_one = [30.0, 40.0, 20.0, 131.0, 161.0, 146.0, 0, -29]
    points1 = dk(touch_one)
    print(points1[-1]) # [-45.294   2.582   4.05 ]
