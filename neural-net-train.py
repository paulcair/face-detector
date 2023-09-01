import tensorflow as tf
import numpy as np
from tensorflow import keras

# Printing stuff
import matplotlib.pyplot as plt

# Load a pre-defined dataset (70k of 28x28)
fashion_mnist = keras.datasets.fashion_mnist

#pull out data from dataset
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

 # Show data
#print(train_labels[0])
#print(train_images[0])
#plt.imshow(train_images[0], cmap='gray', vmin=0, vmax=255)
#plt.show()

# Define our neural net structure
model = keras.Sequential([
    # input is a 28x28 image ("Flatten" flattens the 28x28 into a single 784x1 input layer)
    keras.layers.Flatten(input_shape=(28,28)),

    # hidden layer is 128 deep. relu returns the value, or 0 (works good enough, much faster)
    keras.layers.Dense(units=128, activation=tf.nn.relu), 

    # output is 0-10 (depending on what piece of clithing it is). return maximum
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

# Compile our model
model.compile(optimizer=tf.optimizers.Adam(), loss='sparse_categorical_crossentropy')

# Train our model, using our training data
print()
print('Training the model')
model.fit(train_images, train_labels, epochs=5)

# Test our model, using our testing data
print()
print('Testing the model using the test data to make a prediction')
test_loss = model.evaluate(test_images, test_labels)

# Make predictions matrix for each test image in the matrix of 60000 images
predictions = model.predict(test_images)


# Print the value of prediction for test_image at 0
print()
print(predictions[0])
# Print the highest number in the predictions at image 0
label_number = list(predictions[0]).index(max(predictions[0]))
print(label_number)
# Print the value of prediction for test_image at 0
#print(test_labels[0])

# Create a matrix that holds strings for the labels
name = ['T-shirt', 'Pants', 'Hoodie', 'Dress', 'Coat', 'sandal', 'Shirt', 'Sneaker', 'Bag', 'Shoe']
# Print the name of the test label prediction
print(name[label_number])

# Show the test image at point 0 in the matrix
plt.imshow(test_images[0], cmap='gray', vmin=0, vmax=255)
plt.show()


