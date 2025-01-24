import numpy as np

ind = 1

postures = []
with open(f'blending/blended{ind}.txt','r') as f:
    lines = f.readlines()
    dofs = eval(lines[0])
    for line in lines[1:]:
        posture = eval(line)
        postures.append(posture)

print('loaded',len(postures),'postures')

from dk import dk

trajectory = np.array([ dk(thetas)[0][-1] for thetas in postures ])

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Extract x, y, z coordinates
x = trajectory[:, 0]
y = trajectory[:, 1]
z = trajectory[:, 2]

# Create a 3D plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot the trajectory as a line
ax.plot(x, y, z, label='1', color='blue')

# Optionally, plot the points as small spheres
ax.scatter(x, y, z, color='red', s=20, label='Points')

# Add labels
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('trajectory 1')
ax.legend()

# Show the plot
plt.show()

#==========================================

bp = trajectory[0]
ep = trajectory[-1]
f = np.linspace(0.0,1.0,len(trajectory))
ideal = np.transpose(f*np.expand_dims(ep-bp,1))+bp

# Extract x, y, z coordinates
x = ideal[:, 0]
y = ideal[:, 1]
z = ideal[:, 2]

# Create a 3D plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot the trajectory as a line
ax.plot(x, y, z, label='1', color='blue')

# Optionally, plot the points as small spheres
ax.scatter(x, y, z, color='red', s=20, label='Points')

# Add labels
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('ideal 1')
ax.legend()

# Show the plot
plt.show()

#=======================================

err = np.linalg.norm(trajectory - ideal,axis=1) 

plt.plot(f,err)
plt.show()
