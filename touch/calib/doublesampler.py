import numpy as np
from nicomover import load_movement, save_movement

ns = [
    #
    46, #0
    40, #1
    39, #2
    40, #3
    40, #4
    41, #5
    41, #6
    41, #7
    42, #8
    40, #9
    #
    40, #10
    40, #11
    41, #12
    40, #13
    42, #14
    42, #15
    42, #16
    40, #17
    42, #18
    43, #19
    #
    42, #20
    42, #21
    42, #22
    41, #23
    41, #24
    41, #25
    47, #26
    47, #27
    47, #28
    46, #29
    #
    47, #30
    46, #31
    46, #32
    47, #33
    47, #34
    46, #35
    48, #36
    47, #37
    48, #38
    47, #39
    #
    47, #40
    46, #41
    47, #42
    47, #43
    47, #44
    46, #45
    47, #46
    47, #47
    48, #48
    48, #49
    #
    47, #50
    47, #51
    47, #52
    48, #53
    47, #54
    48, #55
    48, #56
    47  #57
]

dataset = load_movement('dataset.txt')

old_dataset = load_movement('sarah.txt')
dofs = list(old_dataset[0].keys())

start_pose = load_movement('start.txt')[0]

new_dataset = []
for old_sample, sample, n in zip(old_dataset,dataset,ns):
    steps = 50
    pose = subset = {k: old_sample[k] for k in dofs} 
    trajectory  = []
    for s in range(steps + 1):
        t = s / steps
        angles = [round(start_pose[dof] + (pose[dof] - start_pose[dof]) * t, 1) for dof in dofs]
        trajectory.append(dict(zip(dofs, angles)))
    new_sample = sample.copy()
    for dof in trajectory[n]:
        new_sample[dof] = trajectory[n][dof]
    new_sample['n'] = n
    new_dataset.append(new_sample)

save_movement('new_dataset.txt',new_dataset)
