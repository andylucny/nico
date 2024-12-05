postures = []
with open('poses.txt','r') as f:
    for line in f.readlines()[1:]:
        posture = eval(line)
        postures.append(posture)

print('loaded',len(postures),'postures')

from nicomover import enableTorque, play_movement, todicts, move_to_posture, todict, park, setAngle, getAngle
print('started')

carlo_matilde_position_dofs = ['l_shoulder_z', 'l_shoulder_y', 'l_arm_x', 'l_elbow_y', 'l_wrist_z', 'l_wrist_x', 'l_thumb_z', 'l_thumb_x', 'l_indexfinger_x', 'l_middlefingers_x', 'r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x', 'r_thumb_z', 'r_thumb_x', 'r_indexfinger_x', 'r_middlefingers_x']
#carlo_matilde_position_values = [-23.0, 14.0, 0.0, 103.0, -1.0, -55.0, -62.0, -180.0, -179.0, -176.0, -25.0, 83.0, 47.0, 94.0, -59.0, 114.0, -1.0, 44.0, -179.0, 138.0]
carlo_matilde_position_values = [-23.0, 14.0, 0.0, 103.0, -1.0, -55.0, -62.0, -180.0, -179.0, -176.0, -25.0, 83.0, 47.0, 94.0, -59.0, 114.0, -130, 4, 172, 180] # 0.0, 44.0, -179.0, 138.0

enableTorque(carlo_matilde_position_dofs)
play_movement(todicts(carlo_matilde_position_dofs,[carlo_matilde_position_values]),[1])

postures_dofs = ['r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x', 'r_indexfinger_x']

def p(i):
    move_to_posture(todict(postures_dofs,postures[i]))

print('run p(x)')
