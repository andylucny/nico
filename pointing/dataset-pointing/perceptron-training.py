import numpy as np
import keras
from keras.layers import Input
from keras.layers import Dense, Dropout
from keras.models import Model
import cv2

ds = []
with open('pointing_dataset.txt','rt') as f:
    for line in f.readlines():
        d = eval(line[:-1])
        ds.append(d[:-1])

input_names = [f'dino{i}' for i in range(384)] + ['head_z', 'head_y']
output_names = ['r_shoulder_z', 'r_shoulder_y', 'r_arm_x', 'r_elbow_y', 'r_wrist_z', 'r_wrist_x']

names = ds[0]
ds = np.array(ds[1:],np.float32)
input_indices = [names.index(item) for item in input_names if item in names]
sample_inputs = ds[:,input_indices]
output_indices = [names.index(item) for item in output_names if item in names]
sample_outputs = ds[:,output_indices] / 360 + 0.5 # -1 .. 1

inp = Input(shape=(len(input_names),))
x = Dense(50,activation='ReLU')(inp)
x = Dropout(0.2)(x)
x = Dense(50,activation='ReLU')(x)
out = Dense(6,activation='sigmoid')(x)
model = Model(inputs=inp, outputs=out)
model.summary()

model.compile(optimizer=keras.optimizers.Adam(), loss=keras.losses.MeanSquaredError(), metrics=[keras.metrics.MeanSquaredError()])

model.fit(sample_inputs, sample_outputs, batch_size=18, epochs=100)

model.save('../pointing.h5')
print('saved')

# test
results = model.predict(sample_inputs)
for sample, result in zip(sample_outputs, results):
    sample_deg = (sample-0.5)*360
    result_deg = (result-0.5)*360
    print(list(sample-result))

#quit()
