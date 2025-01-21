from dk import dk
from ik import improve
import torch

start_point = [-11.4442,  29.3525,  45.5654]
start_point = torch.tensor(start_point,dtype=torch.float32)

dofs = ['r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x', 'r_indexfinger_x']

touch_postures = {
    1 : [33.01, 40.22, 26.07, 133.93, 109.58, 100.09, -166.81],
    2 : [40.0, 30.02, 28.88, 112.0, 135.43, 149.14, -176.84],
    3 : [58.0, 32.0, 42.15, 131.0, 115.74, 20, -159.69],
    4 : [51.3, 44.7, 38.81, 148.09, 119.16, 50.77, -174.29],
    5 : [38.81, 43.12, 37.32, 145.1, 111.6, 51.38, -176.84],
    6 : [26.33, 33.89, 32.66, 125.67, 117.49, 94.02, -154.59],
    7 : [35.03, 13.58, 43.65, 104.04, 96.57, 92.79, -149.49],
}

ind = 7

touch_posture = torch.tensor(touch_postures[ind],dtype=torch.float32)
touch_point = dk(touch_posture)[0][-1]

N = 50
fractions = (torch.arange(N+1))/N
points = touch_point + fractions.unsqueeze(1) * (start_point - touch_point)

posture = touch_posture
new_postures = []
for point, fraction in zip(points,fractions):
    print()
    print(fraction.item(),'.')
    posture, _, _ = improve(start_point,touch_point,posture,point,200000)
    new_postures.append(posture)

with open(f'generated{ind}.txt','wt') as f:
    f.write(str(dofs)+'\n')
    for posture in new_postures[::-1]:
        f.write(str(posture)+'\n')
