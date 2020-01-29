""" Model Tester Script """
import tensorflow as tf
import matplotlib.pyplot as plt

import numpy as np

new_model = tf.keras.models.load_model('model2.h5')
print(new_model.summary())

# x = imread('output.png', mode='L')
# x = np.invert(x)
# x = imresize(x, (28, 28))

img = np.reshape(xtest[0], (1, 28, 28))
predictions = new_model.predict_classes(img)
print(predictions)
plt.imshow(img.reshape((28, 28)))
plt.show()
