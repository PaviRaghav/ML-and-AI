import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

learning_rate = 0.01
training_epochs = 1000
batch_size = 100
display_step = 100


def inference(x):
    init = tf.constant_initializer(value=0)
    W = tf.get_variable("W", [784,10], initializer=init)
    b = tf.get_variable("b", [10], initializer=init)
    output = tf.nn.softmax(tf.matmul(x, W) + b)
    return output


def loss(output, y):
    dot_product = y * tf.log(output)
    xen = -tf.reduce_sum(dot_product, axis=1)
    return tf.reduce_mean(xen)


def training(cost, step):
    tf.summary.scalar("cost", cost)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train_op1 = optimizer.minimize(cost, global_step=step)
    return train_op1


def evaluate(output, y):
    correct_prediction = tf.cast(tf.equal(tf.argmax(output, 1), tf.argmax(y, 1)), tf.float32)
    accuracy = tf.reduce_mean(correct_prediction)
    tf.summary.scalar("validation error", (1.0 - accuracy))
    return accuracy


with tf.Graph().as_default():
    x = tf.placeholder("float", [None, 784])
    y = tf.placeholder("float", [None, 10])
    output = inference(x)
    cost = loss(output, y)
    global_step = tf.Variable(0, name='global_step', trainable=False)
    train_op = training(cost, global_step)
    eval_op = evaluate(output, y)
    summary_op = tf.contrib.deprecated.merge_all_summaries()
    saver = tf.train.Saver()
    sess = tf.Session()
    summary_writer = tf.summary.FileWriter('LogisticLogs/', graph_def=sess.graph_def)
    init = tf.initialize_all_variables()
    sess.run(init)

    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)
        for i in range(total_batch):
            mbatch_x, mbatch_y = mnist.train.next_batch(batch_size)
            feed_dict = {
                x: mbatch_x,
                y: mbatch_y
            }
            sess.run(train_op,feed_dict=feed_dict)
            minibatch_cost = sess.run(cost,feed_dict=feed_dict)
            avg_cost += minibatch_cost/total_batch
        if epoch % display_step == 0:
            val_feed_dict = {
                x: mnist.validation.images,
                y: mnist.validation.labels
            }
            accuracy = sess.run(eval_op, feed_dict=val_feed_dict)
            if epoch % 100 == 0:
                print("validation accuracy : ", accuracy)
            summary_str = sess.run(summary_op, feed_dict=feed_dict)
            summary_writer.add_summary(summary_str, sess.run(global_step))
            saver.save(sess, 'LogisticLogs/model-checkpoint', global_step=global_step)
    print("Optimization Finished")
    test_feed_dict = {
        x: mnist.test.images,
        y: mnist.test.labels
    }
    accuracy = sess.run(eval_op, feed_dict=test_feed_dict)
    print("test accuracy : ", accuracy)
