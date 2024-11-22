from keras.models import load_model
import numpy as np

model = load_model('movement.h5')
fractions = np.linspace(0,1,51)
postures_dofs = ['r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x']
postures_values = np.array(model(fractions) * 180)

from nicomover import enableTorque, play_movement, todicts, move_to_posture, todict, park

carlo_matilde_position_dofs = ['l_shoulder_z', 'l_shoulder_y', 'l_arm_x', 'l_elbow_y', 'l_wrist_z', 'l_wrist_x', 'l_thumb_z', 'l_thumb_x', 'l_indexfinger_x', 'l_middlefingers_x', 'r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x', 'r_thumb_z', 'r_thumb_x', 'r_indexfinger_x', 'r_middlefingers_x']
carlo_matilde_position_values = [-23.0, 14.0, 0.0, 103.0, -1.0, -55.0, -62.0, -180.0, -179.0, -176.0, -25.0, 83.0, 47.0, 94.0, -59.0, 114.0, -1.0, 44.0, -179.0, 138.0]
enableTorque(carlo_matilde_position_dofs)
def m0():
    play_movement(todicts(carlo_matilde_position_dofs,[carlo_matilde_position_values]),[1])

m0()

def m1(duration = 2):
    n = len(fractions)
    play_movement(todicts(postures_dofs,postures_values),[duration/n]*n)

def p(i):
    move_to_posture(todict(postures_dofs,postures_values[i]))
