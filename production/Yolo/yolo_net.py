import numpy as np
import tensorflow as tf
slim = tf.contrib.slim
import inspect

class YOLONet(object):

    def __init__(self):
        self.classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
                   'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse',
                   'motorbike', 'person', 'pottedplant', 'sheep', 'sofa',
                   'train', 'tvmonitor']
        self.scale = 1.0 * 448 / 7

        self.offset = np.transpose(np.reshape(np.array([np.arange(7)] * 7 * 2),(2, 7, 7)), (1, 2, 0))

        self.images = tf.placeholder(tf.float32, [None, 448, 448, 3],name='images')
        self.logits = self.build_network(self.images)


    def build_network(self,images,scope='yolo'):
        with tf.variable_scope("yolo"):
            net = tf.pad(images, np.array([[0, 0], [3, 3], [3, 3], [0, 0]]))

            net = conv2d(net, tf.get_variable("conv_2/weights", [7,7,3,64]),tf.get_variable("conv_2/biases", [64]),strides = 2,padding="VALID")

            net = slim.max_pool2d(net, 2, padding='SAME')

            net = conv2d(net, tf.get_variable("conv_4/weights", [3,3,64,192]),tf.get_variable("conv_4/biases", [192]))

            net = slim.max_pool2d(net, 2, padding='SAME')

            net = conv2d(net, tf.get_variable("conv_6/weights", [1,1,192,128]),tf.get_variable("conv_6/biases", [128]))
            net = conv2d(net, tf.get_variable("conv_7/weights", [3,3,128,256]),tf.get_variable("conv_7/biases", [256]))
            net = conv2d(net, tf.get_variable("conv_8/weights", [1,1,256,256]),tf.get_variable("conv_8/biases", [256]))
            net = conv2d(net, tf.get_variable("conv_9/weights", [3,3,256,512]),tf.get_variable("conv_9/biases", [512]))
            
            net = slim.max_pool2d(net, 2, padding='SAME')

            net = conv2d(net, tf.get_variable("conv_11/weights", [1,1,512,256]),tf.get_variable("conv_11/biases", [256]))
            net = conv2d(net, tf.get_variable("conv_12/weights", [3,3,256,512]),tf.get_variable("conv_12/biases", [512]))
            net = conv2d(net, tf.get_variable("conv_13/weights", [1,1,512,256]),tf.get_variable("conv_13/biases", [256]))
            net = conv2d(net, tf.get_variable("conv_14/weights", [3,3,256,512]),tf.get_variable("conv_14/biases", [512]))
            net = conv2d(net, tf.get_variable("conv_15/weights", [1,1,512,256]),tf.get_variable("conv_15/biases", [256]))
            net = conv2d(net, tf.get_variable("conv_16/weights", [3,3,256,512]),tf.get_variable("conv_16/biases", [512]))
            net = conv2d(net, tf.get_variable("conv_17/weights", [1,1,512,256]),tf.get_variable("conv_17/biases", [256]))
            net = conv2d(net, tf.get_variable("conv_18/weights", [3,3,256,512]),tf.get_variable("conv_18/biases", [512]))
            net = conv2d(net, tf.get_variable("conv_19/weights", [1,1,512,512]),tf.get_variable("conv_19/biases", [512]))
            net = conv2d(net, tf.get_variable("conv_20/weights", [3,3,512,1024]),tf.get_variable("conv_20/biases", [1024]))

            net = slim.max_pool2d(net, 2, padding='SAME')

            net = conv2d(net, tf.get_variable("conv_22/weights", [1,1,1024,512]),tf.get_variable("conv_22/biases", [512]))
            net = conv2d(net, tf.get_variable("conv_23/weights", [3,3,512,1024]),tf.get_variable("conv_23/biases", [1024]))
            net = conv2d(net, tf.get_variable("conv_24/weights", [1,1,1024,512]),tf.get_variable("conv_24/biases", [512]))
            net = conv2d(net, tf.get_variable("conv_25/weights", [3,3,512,1024]),tf.get_variable("conv_25/biases", [1024]))
            net = conv2d(net, tf.get_variable("conv_26/weights", [3,3,1024,1024]),tf.get_variable("conv_26/biases", [1024]))

            net = tf.pad(net, np.array([[0, 0], [1, 1], [1, 1], [0, 0]]))

            net = conv2d(net, tf.get_variable("conv_28/weights", [3,3,1024,1024]),tf.get_variable("conv_28/biases", [1024]),strides = 2, padding='VALID')
            net = conv2d(net, tf.get_variable("conv_29/weights", [3,3,1024,1024]),tf.get_variable("conv_29/biases", [1024]))
            net = conv2d(net, tf.get_variable("conv_30/weights", [3,3,1024,1024]),tf.get_variable("conv_30/biases", [1024]))

            net = tf.transpose(net, [0, 3, 1, 2], name='trans_31')
            net = tf.reshape(net, [-1,50176])

            net = fully_connected(net, tf.get_variable("fc_33/weights",[50176,512]), tf.get_variable("fc_33/biases",[512]), activaten_function=True)
            net = fully_connected(net, tf.get_variable("fc_34/weights",[512,4096]), tf.get_variable("fc_34/biases",[4096]), activaten_function=True)
            net = fully_connected(net, tf.get_variable("fc_36/weights",[4096,1470]), tf.get_variable("fc_36/biases",[1470]))
        return net

def fully_connected(x, W, b, activaten_function= False):
    x = tf.add(tf.matmul(x, W), b)
    if activaten_function:
        x = tf.nn.leaky_relu(x, alpha=0.1, name='leaky_relu')
    return x

def conv2d(x, W, b, strides=1, padding="SAME"):
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding=padding)
    x = tf.nn.bias_add(x, b)
    return tf.nn.leaky_relu(x, alpha=0.1, name='leaky_relu')

def leaky_relu(alpha):
    def op(inputs):
        return tf.nn.leaky_relu(inputs, alpha=alpha, name='leaky_relu')
    return op
