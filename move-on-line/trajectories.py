import time
from keras.models import load_model
import numpy as np
from nicomover import enableTorque, play_movement, todicts, move_to_posture, todict, park
print('started')

duration = 2.0
ind = 1 
print(ind)
    
model = load_model(f'{ind}.h5')
fractions = np.linspace(0,1.0,51)
postures_dofs = ['r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x', 'r_indexfinger_x']
postures_values = np.array(model(fractions) * 180)

carlo_matilde_position_dofs = ['l_shoulder_z', 'l_shoulder_y', 'l_arm_x', 'l_elbow_y', 'l_wrist_z', 'l_wrist_x', 'l_thumb_z', 'l_thumb_x', 'l_indexfinger_x', 'l_middlefingers_x', 'r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x', 'r_thumb_z', 'r_thumb_x', 'r_indexfinger_x', 'r_middlefingers_x']
enableTorque(carlo_matilde_position_dofs)

play_movement(todicts(['r_thumb_z', 'r_thumb_x', 'r_middlefingers_x'],[[-180,-40,180]]),[1])
play_movement(todicts(postures_dofs,[postures_values[0]]),[duration])

def run():
    for _ in range(10):
        n = len(postures_values)
        play_movement(todicts(postures_dofs,postures_values),[duration/n]*n)
        time.sleep(1)
        n = len(postures_values)
        play_movement(todicts(postures_dofs,postures_values[::-1]),[duration/n]*n)
        time.sleep(1)

#run()
#park()
