""" Model Tester Script """
import tensorflow as tf
import matplotlib.pyplot as plt

import numpy as np

mnist = tf.keras.datasets.mnist
(xtrain, ytrain), (xtest, ytest) = mnist.load_data()

xtrain = tf.keras.utils.normalize(xtrain, axis=1)
xtest = tf.keras.utils.normalize(xtest, axis=1)

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = tf.keras.models.model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")

loaded_model.compile(optimizer='adam',
                     loss='sparse_categorical_crossentropy',
                     metrics=['accuracy'])

# x = imread('output.png', mode='L')
# x = np.invert(x)
# x = imresize(x, (28, 28))

img = np.reshape(xtest[0], (1, 28, 28))
predictions = loaded_model.predict_classes(img)
print(predictions)
plt.imshow(img.reshape((28, 28)))
plt.show()
