""" Model Compiler Script """
import tensorflow as tf

mnist = tf.keras.datasets.mnist
(xtrain, ytrain), (xtest, ytest) = mnist.load_data()

xtrain = tf.keras.utils.normalize(xtrain, axis=1)
xtest = tf.keras.utils.normalize(xtest, axis=1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))


model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(xtrain, ytrain, epochs=15)

model_json = model.to_json()
with open("model.json", "w") as json_file:
  json_file.write(model_json)
model.save("model2.h5")

print("Saved model to disk")
