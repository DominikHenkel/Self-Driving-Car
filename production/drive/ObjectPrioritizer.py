import tensorflow as tf
import numpy as np

def __init__():


def recurrent_network():
    hidden_size = 100
    seq_length = 5
    learning_rate = 1e-1

    with tf.variable_scope("yolo"):
        input_hidden = tf.get_variable('l1',[hidden_size, 5])
        hidden_hidden = tf.get_variable('l2',[hidden_size,hidden_size])
        hidden_output = tf.get_variable('l3',[hidden_size,hidden_size])
        bias_hidden = tf.get_variable('b1', [hidden_size,1], initializer=tf.zeros_initializer())
        bias_output = tf.get_variable('b2', [hidden_size,1], initializer=tf.zeros_initializer())
