from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt

ind = 7
model = load_model(f'{ind}.h5')

fractions = np.linspace(0,1.0,51)
postures_dofs = ['r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x', 'r_indexfinger_x']
postures_values = np.array(model(fractions) * 180)

with open(f'modeled{ind}.txt','wt') as f:
    f.write(str(postures_dofs)+'\n')
    for posture in postures_values:
        f.write(str([angle for angle in posture])+'\n')
