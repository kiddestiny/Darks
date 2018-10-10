from threading import Thread
import time

# IO
def music():
    print('begin to listen music {}'.format(time.ctime()))
    time.sleep(3)
    print('stop to listen music {}'.format(time.ctime()))


def game():
    print('begin to play game {}'.format(time.ctime()))
    time.sleep(5)
    print('stop to play game {}'.format(time.ctime()))

# CPU 
def add():
    sum = 0
    i = 1
    while i<=1000000:
        sum += i
        i += 1
    print('sum:',sum)


def mul():
    sum2 = 1
    i = 1
    while i<=100000:
        sum2 = sum2 * i
        i += 1
    print('sum2:',sum2)


if __name__ == '__main__':
    start = time.time()
    t1 = Thread(target=add)
    t2 = Thread(target=mul)
    # sequence cost time 4.990154027938843
    # add()
    # mul()
    t1.start() 
    t2.start()
    t2.join()
    print('cost time {}'.format(time.time()-start))

#    t1 = Thread(target=music) #创建一个线程对象t1 子线程
#    t2 = Thread(target=game) #创建一个线程对象t2 子线程
#
#    t1.start()
#    t2.start()
#
#    # t1.join() #等待子线程执行完 t1不执行完，谁也不准往下走
#    t2.join()

#    print('ending.......') #主线程
#    print(time.ctime())
