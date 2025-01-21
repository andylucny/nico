import numpy as np
import time

ind = 7

postures1 = []
with open(f'modeled{ind}.txt','r') as f:
    lines = f.readlines()
    dofs = eval(lines[0])
    for line in lines[1:]:
        posture = eval(line)
        postures1.append(posture)

postures2 = []
with open(f'generated{ind}.txt','r') as f:
    lines = f.readlines()
    dofs = eval(lines[0])
    for line in lines[1:]:
        posture = eval(line)
        postures2.append(posture)

print('loaded',len(postures1),'and',len(postures2),'postures')

fractions = np.linspace(0,1,len(postures1))
postures = []
for posture1, posture2, fraction in zip(np.array(postures1), np.array(postures2), fractions):
    posture = posture1 * (1-fraction) + posture2 * fraction
    postures.append(posture)

with open(f'blended{ind}.txt','w') as f:
    f.write(str(dofs)+'\n')
    for posture in postures:
        f.write(str(list(posture))+'\n')
