import tensorflow as tf

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

def normalize(data):
    return tf.keras.utils.normalize(data, axis=1)

x_train = normalize(x_train)
x_test = normalize(x_test)


model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=x_train[0].shape))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

model.compile(optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
        )
model.fit(x_train, y_train, epochs=3)

model.save('epic_number_reader.model')

new_model = tf.keras.models.load_model('epic_number_reader.model')

val_loss, val_acc = new_model.evaluate(x_test, y_test)
print(val_loss, val_acc)

import matplotlib.pyplot as plt

plt.imshow(x_train[0], cmap=plt.cm.binary)
plt.show()
#print(x_train[0])

predictions = new_model.predict([x_test])

import numpy as np
print(np.argmax(predictions[0]))

plt.imshow(x_test[0])
plt.show()
