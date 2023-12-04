import numpy as np
import os
import random
# import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from keras.models import load_model


CommandList = {'five.txt': 5, 'one.txt': 1, 'two.txt': 2, 'zero.txt': 0, 'pinch.txt': 11, 'tap.txt': 12,
               'five1.txt': 5, 'one1.txt': 1, 'two1.txt': 2, 'zero1.txt': 0, 'pinch1.txt': 11, 'tap1.txt': 12}


def read_data(train_test_proportion=0.85):
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    for fileName in os.listdir('datas'):
        filePath = 'datas/' + fileName
        y = CommandList[fileName]
        with open(filePath, 'r') as f:
            for line in f.readlines():
                try:
                    # print(type(eval(line)))
                    x = eval(line)
                except:
                    continue

                if random.random() <= train_test_proportion:
                    x_train.append(x)
                    y_train.append(y)
                else:
                    x_test.append(x)
                    y_test.append(y)

    x_train = np.array(x_train)
    y_train = np_utils.to_categorical(np.array(y_train), num_classes=13)
    x_test = np.array(x_test)
    y_test = np_utils.to_categorical(np.array(y_test), num_classes=13)
    # print('data got:')
    # print(x_train.shape)
    # print(y_train.shape)
    # # print(y_train)
    # print(x_test.shape)
    # print(y_test.shape)

    return x_train, y_train, x_test, y_test


model = Sequential()

model.add(Dense(units=64, activation='relu', input_dim=65))
model.add(Dense(units=128, activation='relu'))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=13, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])
# model.compile(loss=keras.losses.categorical_crossentropy,
#               optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True),
#               metrics=['accuracy'])


x_train, y_train, x_test, y_test = read_data()
model.fit(x_train, y_train, epochs=1024, batch_size=32)

loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)
print(loss_and_metrics)

# model.save('my_model.keras')
model.save_weights('my_model_weights.h5')

# del model
# model = load_model('my_model.h5')
model.load_weights('my_model_weights.h5')
x_train, y_train, x_test, y_test = read_data(train_test_proportion=0.1)
loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)
print(loss_and_metrics)


