import numpy as np
import time
from nicomover import load_movement, park, move_to_posture, move_to_posture_through_time, save_movement

from TouchAgent import TouchAgent, draw
time.sleep(1)
TouchAgent()
time.sleep(1)

start_pose = load_movement('start.txt')[0]
move_to_posture(start_pose)
time.sleep(2)

dataset = load_movement('dataset.txt')
indices = list(dataset[0].keys())
dofs = indices[:-3]
ds = np.array([[sample[index] for index in indices] for sample in dataset])

for i, sample in enumerate(ds):
    posture = sample[:-3]
    x, y, n = sample[-3:]
    draw(f'{i}/{int(n)}',(int(2400*x), int(1350*y)))
    move_to_posture(dict(zip(dofs,posture)))
    time.sleep(2)

