import time

import matplotlib.pyplot as plt
from numpy import asarray, unique, argmax
from tensorflow.keras.datasets.mnist import load_data
from tensorflow.keras import Sequential
from tensorflow.keras.layers import (
                                    Dense,
                                    Conv2D,
                                    MaxPool2D,
                                    Flatten,
                                    Dropout
                                    )

# Cargamos el dataset MNIST
(x_train, y_train), (x_test, y_test) = load_data()
print(f'Train: X={x_train.shape}, y={y_train.shape}')
print(f'Test: X={x_test.shape}, y={y_test.shape}')

# hacemos un reshape a los datos y lo pasamos a un solo canal
x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], x_train.shape[2], 1))
x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], x_test.shape[2], 1))

# normalizando los pixeles
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# estableciendo la forma de la imagen de entrada
input_shape = x_train.shape[1:]

# estableciendo el número de clases
n_classes = len(unique(y_train))

# definiendo el modelo
model = Sequential()
model.add(Conv2D(64, (3,3), activation='relu', input_shape=input_shape))
model.add(MaxPool2D((2, 2)))
model.add(Conv2D(32, (3,3), activation='relu'))
model.add(MaxPool2D((2, 2)))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(n_classes, activation='softmax'))

# definiendo la pérdida y el optimizador
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# entrenando el modelo
model.fit(x_train, y_train, epochs=10, batch_size=128, verbose=1)

# evaluando el modelo
loss, acc = model.evaluate(x_test, y_test, verbose=0)
print('Accuracy: %.3f' % acc)

# guardando el modelo
ts = int(time.time())
file_path = f"./img_classifier/{ts}/"
model.save(filepath=file_path, save_format='tf')
print("Modelo guardado\n")