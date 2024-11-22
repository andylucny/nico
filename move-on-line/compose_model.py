import keras
from keras.models import load_model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Concatenate
from keras.models import Model

ms = []
for i in range(6):
    m = load_model(f'movement{i+1}.h5')
    m._name = f'model{i+1}'
    ms.append(m)

inp = Input(shape=(1,))
xs = [ m(inp) for m in ms ]
out = Concatenate()(xs)

model = Model(inputs=inp, outputs=out)
model.summary()

model.compile(optimizer=keras.optimizers.Adam(), loss=keras.losses.MeanSquaredError(), metrics=[keras.metrics.MeanSquaredError()])

model.save('movement.h5')
