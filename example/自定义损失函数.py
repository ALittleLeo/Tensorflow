import tensorflow as tf
from numpy.random import RandomState
batch_size = 8

#两个输入节点
x = tf.placeholder(tf.float32, shape=(None, 2), name='x-input')
#回归问题一般只有一个输出节点
y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y-input')

#定义一个单层的神经网络前向传播过程，这里就是简单加权和
w1 = tf.Variable(tf.random_normal([2, 1], stddev=1, seed=1))
y = tf.matmul(x, w1)

#定义预测多了和预测少了的成本
loss_less = 10
loss_more = 1
#tf.grater()比较张量中对应元素的大小，返回true或者false
#tf.where()第一个参数是true时，选择第二个参数，否侧选择第三个参数
loss = tf.reduce_sum(tf.where(tf.greater(y, y_),(y-y_)*loss_more, (y_-y)*loss_less))
train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

#通过随机数生成一个模拟数据集
rdm = RandomState(1)
dataset_size = 128
X = rdm.rand(dataset_size, 2)
# 设置回归的正确值为两个输入的和加上一个随机量。之所以要加上一个随机量
# 是为了加入不可消除的噪音，否则不同损失函数的意义就不大了，因为不同损失函数
# 都会在能完全预测正确的时候最低。一般来说噪音为一个均值为0的小量，所以这里的噪声
# 设置为-0.05~0.05的随机数
Y = [[x1 + x2 + rdm.rand()/10.0-0.05] for (x1, x2) in X]
#训练神经网络
with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    print(sess.run(w1))
    STEPS = 5000
    for i in range(STEPS):
        start = (i*batch_size) % dataset_size
        end = min(start+batch_size, dataset_size)
        sess.run(train_step, feed_dict={x: X[start:end], y_:Y[start:end]})
    print(sess.run(w1))