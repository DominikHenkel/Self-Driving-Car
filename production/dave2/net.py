import numpy as np
import tensorflow as tf
import cv2

def __init__():
    x = tf.placeholder(tf.float32, [None,200, 66, 3])
    y = tf.placeholder(tf.float32, [None,1])
    keep_prob = tf.placeholder(tf.float32)

    pred = build_network(x, keep_prob)

    # Define loss and optimizer
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = pred, labels = y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    # Evaluate model
    correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # Initializing the variables
    init_op = tf.initialize_all_variables()

    sess = tf.Session()
    sess.run(init_op)

    cap = cv2.VideoCapture(0)

    while(True):
        ret, frame = cap.read()

        resized_frame = cv2.resize(frame, (66, 200))
        resized_frame = np.resize(frame,(1,200,66,3))
        cv2.imshow('frame',frame)

        print(sess.run(pred, feed_dict={x: resized_frame, keep_prob: 1}))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def build_network(frame,dropout):
    print(frame.shape)
    net = tf.reshape(frame, shape=[-1, 200,66,3])

    net = conv2d(frame, tf.Variable(tf.truncated_normal([5,5,3,24], dtype=tf.float32)),tf.Variable(tf.truncated_normal([24], dtype=tf.float32)),strides = 2)
    net = conv2d(net, tf.Variable(tf.truncated_normal([5,5,24,36], dtype=tf.float32)),tf.Variable(tf.truncated_normal([36], dtype=tf.float32)),strides = 2)
    net = conv2d(net, tf.Variable(tf.truncated_normal([5,5,36,48], dtype=tf.float32)),tf.Variable(tf.truncated_normal([48], dtype=tf.float32)),strides = 2)
    net = conv2d(net, tf.Variable(tf.truncated_normal([3,3,48,64], dtype=tf.float32)),tf.Variable(tf.truncated_normal([64], dtype=tf.float32)))
    net = conv2d(net, tf.Variable(tf.truncated_normal([3,3,64,64], dtype=tf.float32)),tf.Variable(tf.truncated_normal([64], dtype=tf.float32)))
    print(net.shape)
    net = tf.nn.dropout(net, 0.5)

    net = tf.reshape(net, [-1,100])

    net = fully_connected(net, tf.Variable(tf.truncated_normal([100,50], dtype=tf.float32)), tf.Variable(tf.truncated_normal([50], dtype=tf.float32)), activaten_function=True)
    net = fully_connected(net, tf.Variable(tf.truncated_normal([50,10], dtype=tf.float32)), tf.Variable(tf.truncated_normal([10], dtype=tf.float32)), activaten_function=True)
    net = fully_connected(net, tf.Variable(tf.truncated_normal([10,1], dtype=tf.float32)), tf.Variable(tf.truncated_normal([1], dtype=tf.float32)), activaten_function=True)

    return net

def fully_connected(x, W, b, activaten_function= False):
    x = tf.add(tf.matmul(x, W), b)
    if activaten_function:
        x = tf.nn.elu(x)
    return x

def conv2d(x, W, b, strides=1, padding="SAME"):
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding=padding)
    x = tf.nn.bias_add(x, b)
    return tf.nn.elu(x)

if __name__ == "__main__":
    __init__()
