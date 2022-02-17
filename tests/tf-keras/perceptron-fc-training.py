import numpy as np
import keras
from keras.layers import Input
from keras.layers import Conv2D
from keras.models import Model

samples_inp = np.array([[1,2,3],[1,1,1],[4,4,4],[9,9,9],[3,2,1],[0,0,1],[0,0,0]])
samples_out = np.array([[123],[111],[444],[999],[321],[1],[0]])

print(samples_inp.shape)
samples_inp = np.expand_dims(samples_inp,axis=1)
samples_inp = np.expand_dims(samples_inp,axis=1)
print(samples_inp.shape)

print(samples_out.shape)
samples_out = np.expand_dims(samples_out,axis=1)
samples_out = np.expand_dims(samples_out,axis=1)
print(samples_out.shape)

inp = Input(shape=(1,1,3))
mid = Conv2D(10,(1,1),activation='linear')(inp)
out = Conv2D(1,(1,1),activation='linear')(mid)
model = Model(inputs=inp, outputs=out)
model.summary()

model.compile(optimizer='adam', loss='mse', metrics=['mse', 'mae'])

model.fit(samples_inp, samples_out, batch_size=3, epochs=18500)

model.save('perceptron-fc.h5')

print(model.layers[1].get_weights())
print(model.layers[2].get_weights())

# test
result = model.predict(np.array([[[[7,7,7]]]]))
print('test result',result[0])

# test
result = model.predict(np.array([[[[7,7,7],[6,6,6]]]]))
print('test result',result[0])

#quit()
