from mxnet import autograd, nd

#x = nd.arange(12)
#x = x.reshape((-1,4))
#
#tensor = nd.zeros((2, 3, 4))
#
#
#n = nd.random.normal(0, 1, shape=(3, 4))
#
#y = nd.array([[2, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]])
#
#
#nd.dot(x,y.T)
#

x = nd.arange(4).reshape((4, 1))
x.attach_grad()

with autograd.record():
    y = 2 * nd.dot(x.T, x)

y.backward()

assert (x.grad - 4 * x).norm().asscalar() == 0

