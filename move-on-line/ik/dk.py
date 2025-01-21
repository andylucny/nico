import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import time

device='cpu'

def rad(value):
    return value * torch.pi / 180.0

def Txyz(tx, ty, tz):
    tr = torch.eye(4).to(device)
    tr[0,3] = tx
    tr[1,3] = ty
    tr[2,3] = tz
    return tr

def Rz(theta):
    theta = rad(theta)
    tr = torch.eye(4).to(device)
    tr[0,0] = torch.cos(theta)
    tr[0,1] = -torch.sin(theta)
    tr[1,0] = torch.sin(theta)
    tr[1,1] = torch.cos(theta)
    return tr

def Rx(alpha):
    alpha = rad(alpha)
    tr = torch.eye(4).to(device)
    tr[1,1] = torch.cos(alpha)
    tr[1,2] = -torch.sin(alpha)
    tr[2,1] = torch.sin(alpha)
    tr[2,2] = torch.cos(alpha)
    return tr

def Ry(beta):
    beta = rad(beta)
    tr = torch.eye(4).to(device)
    tr[0,0] = torch.cos(beta)
    tr[0,2] = torch.sin(beta)
    tr[2,0] = -torch.sin(beta)
    tr[2,2] = torch.cos(beta)
    return tr

def Ts(thetas):
    t90 = torch.tensor(90.0).to(device)
    t180 = torch.tensor(180.0).to(device)
    return [
        Txyz(0,5,19.5), Rz(t90), Rz(thetas[0]), # -> 'r_shoulder_z'
        Txyz(0,-1.5,2.5), Ry(t90), Rz(thetas[1]), # -> 'r_shoulder_y'
        Txyz(3,0,9.5), Rx(-t90), Rz(-thetas[2]), # -> 'r_arm_x'
        Txyz(17.5,0,0), Rx(t90), Rz(t180), Rz(-thetas[3]), # -> 'r_elbow_y'
        Txyz(10,0,0), Ry(t90), Rz(-thetas[4]/2.0), # -> 'r_wrist_z'
        Txyz(0,0,10), Rx(-t90), Rz(-t90), Rz(thetas[5]/4.5+10), # -> 'r_wrist_x'
        Txyz(0,-1,0), Txyz(6,0,0), Rz(20+(thetas[6]+180)/4.5), Txyz(6,0,0), Ry(t90) # -> 'r_indexfinger_x'
    ]

def dk(thetas):
    point0 = torch.tensor([[0., 0., 0., 1.0]], dtype=torch.float32, requires_grad=False).T.to(device)
    vector0 = torch.tensor([[0., 0., 1.0]], dtype=torch.float32, requires_grad=False).T.to(device)
    e = torch.eye(4, dtype=torch.float32, requires_grad=False).to(device)
    points = [point0.T[0][:3]]
    vectors = [vector0]
    re = e
    for T in Ts(thetas):
        re = re @ T
        points.append((re @ point0).T[0][:3])
        vectors.append( (re[:3,:3] @ vector0).T[0] )

    return points, vectors
