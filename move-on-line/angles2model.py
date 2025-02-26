import numpy as np
np.set_printoptions(precision=3,suppress=True)
from dk import dk

def closest_fraction_on_line(A, B, C):
    # Convert points to NumPy arrays
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    # Vector from A to B and from A to C
    AB = B - A
    AC = C - A
    # Calculate the fraction t (projection of AC onto AB, normalized)
    t = np.dot(AC, AB) / np.dot(AB, AB)
    # Clamp t to be within the range [0, 1] if point must be on the segment
    t = np.clip(t, 0, 1)
    return t

ind = 1
postures = []
with open(f'{ind}{ind}.txt','r') as f:
    for line in f.readlines()[1:]:
        posture = eval(line)
        postures.append(posture)

point_carlo_matilde = dk(postures[0])[0][-1]
point_touch = dk(postures[-1])[0][-1]
fractions = []
for posture in postures:
    point = dk(posture)[0][-1]
    fraction = closest_fraction_on_line(point_carlo_matilde,point_touch,point)
    fractions.append(fraction)

print(np.array(fractions))

import keras
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Concatenate
from keras.models import Model
#from keras.initializers import GlorotUniform
from tensorflow.keras.callbacks import ReduceLROnPlateau

for index in range(7):

    samples_inp = np.array(fractions,np.float32).reshape(-1,1)
    samples_out = np.array(postures,np.float32)[:,index:index+1]/180.0

    inp = Input(shape=(1,))
    #outs = []
    #for _ in range(6):
    x = Dense(100,activation='ReLU')(inp) 
    #x = Dropout(0.1)(x)
    x = Dense(100,activation='ReLU')(x) 
    #x = Dropout(0.1)(x)
    out = Dense(1,activation='linear')(x)
    #    outs.append(out)
    #out = Concatenate()(outs)
    model = Model(inputs=inp, outputs=out)
    model.summary()

    model.compile(optimizer=keras.optimizers.Adam(), loss=keras.losses.MeanSquaredError(), metrics=[keras.metrics.MeanSquaredError()])

    # Define the ReduceLROnPlateau callback
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',      # Metric to monitor
        factor=0.75,              # Factor by which to reduce the learning rate (0.5 means it will halve it)
        patience=10,              # Number of epochs to wait before reducing the learning rate
        min_lr=1e-8,             # Minimum learning rate
        verbose=1                # Print information when learning rate is reduced
    )

    model.fit(
        samples_inp, 
        samples_out, 
        validation_data=(samples_inp, samples_out),
        batch_size=len(postures), 
        epochs=500, 
        #callbacks=[reduce_lr] 
    )

    out = model.predict(samples_inp)
    print((out - samples_out)*180)

    model.save(f'movement{index+1}.h5')


from keras.models import load_model

ms = []
for i in range(7):
    m = load_model(f'movement{i+1}.h5')
    m._name = f'model{i+1}'
    ms.append(m)

inp = Input(shape=(1,))
xs = [ m(inp) for m in ms ]
out = Concatenate()(xs)

model = Model(inputs=inp, outputs=out)
model.summary()

model.compile(optimizer=keras.optimizers.Adam(), loss=keras.losses.MeanSquaredError(), metrics=[keras.metrics.MeanSquaredError()])

model.save(f'{ind}{ind}.h5')
print('\7')
