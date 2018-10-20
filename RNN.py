import tensorflow as tf

tf.reset_default_graph()

n_steps =  28
n_inputs =  28
n_neurons =  150
n_outputs =  10

learning_rate =  0.001
keep_prob = 0.5

X = tf.placeholder(tf.float32, [ None , n_steps, n_inputs])
y = tf.placeholder(tf.int32, [ None ])

#rnn + fuuly connected layer use dropout and xavier
basic_cell = tf.contrib.rnn.BasicRNNCell( num_units = n_neurons)
#cell_drop = tf.contrib.rnn.DropoutWrapper(basic_cell,input_keep_prob=keep_prob)
outputs, states = tf.nn.dynamic_rnn(basic_cell, X, dtype = tf.float32)
#fully connected
xavier_weight = tf.contrib.layers.xavier_initializer(seed=42)
logits = tf.layers.dense(states, n_outputs,kernel_initializer=xavier_weight)

xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits( labels = y,
                                                           logits = logits)
loss = tf.reduce_mean(xentropy)
optimizer = tf.train.AdamOptimizer( learning_rate = learning_rate)
training_op = optimizer.minimize(loss)
correct = tf.nn.in_top_k(logits, y, 1 )
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

init = tf.global_variables_initializer()

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/")
X_test = mnist.test.images.reshape(( - 1 , n_steps, n_inputs))
y_test = mnist.test.labels

n_epochs = 100
batch_size = 150

with tf.Session() as sess:
    init.run()
    for epoch in range(n_epochs):

        for iteration in range(mnist.train.num_examples // batch_size):
            X_batch, y_batch = mnist.train.next_batch(batch_size)
            X_batch = X_batch.reshape((- 1, n_steps, n_inputs))
            sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
        acc_train = accuracy.eval(feed_dict={X: X_batch, y: y_batch})
        acc_test = accuracy.eval(feed_dict={X: X_test, y: y_test})
        print(epoch, " Train accuracy: ", acc_train, " Test accuracy: ", acc_test)