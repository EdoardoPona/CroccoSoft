"""A convolutional autoencoder"""
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow.examples.tutorials.mnist import input_data
import utils 
import cv2


# mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

im_w = 96
im_h = 54
im_ch = 3       # number of color channels
images = utils.get_image_data('me', size=[im_w, im_h])          # returns all the images in the 'me/' directory
print 'Finished loading data'


# helper functions for weights and biases
def weight(shape):
    return tf.Variable(tf.truncated_normal(shape=shape, stddev=0.2))


def bias(shape):
    return tf.Variable(tf.constant(0.1, shape=shape))


# helper functions for convolution and pooling
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def deconv2d(x, W, shape):
    return tf.nn.conv2d_transpose(x, W, strides=[1, 1, 1, 1], padding='SAME', output_shape=shape)


def max_pool(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def avg_pool(x):
    return tf.nn.avg_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def save_image(image, filename):
    cv2.imwrite(filename, image)


def plot(img):
    plt.imshow(img)
    plt.show()


batch_size = 50
x = tf.placeholder(tf.float32, shape=[None, im_h, im_w, im_ch])

# encoder weights and biases
w_conv1 = weight([15, 15, im_ch, 300])            # the first two dimensions are the patch size, then the n of inputs and outputs
b_conv1 = bias([300])

b_deconv1 = bias([im_ch])


# encoder
# x_image = tf.reshape(x, [-1, im_w, im_h, 1])        # 1 is the color channel
h_conv1 = tf.nn.relu(conv2d(x, w_conv1) + b_conv1)


# decoder
output = tf.nn.relu(deconv2d(h_conv1, w_conv1, [tf.shape(x)[0], im_h, im_w, im_ch]) + b_deconv1)    # using relu gives better results 


# cost and optimizer

cost = tf.div(tf.reduce_mean(tf.square(tf.subtract(output, x))), 2)   # mean squared error
train_step = tf.train.AdamOptimizer(5e-4).minimize(cost)

run_list = [train_step, cost]

sess = tf.Session()
sess.run(tf.global_variables_initializer())

# training
batch_size = 100
n_iters = 1000           
print 'Starting Training'
for i in xrange(n_iters):
    # data = mnist.train.next_batch(batch_size)[0]        # [0] are the images, [1] are the labels which we don't need
    data = utils.get_batch_only_imgaes(batch_size, images)
    _, cost = sess.run(run_list, feed_dict={x: data})           # performing train_step, getting the cost

    if i % 5 == 0 or i==n_iters:
        print 'Iteration: {0} Cost: {1}'.format(i, cost)
        
# testing once 
array = utils.get_batch_only_imgaes(batch_size, images)
output = sess.run(output, feed_dict={x: array})

plot(array[0])
plot(output[0])
