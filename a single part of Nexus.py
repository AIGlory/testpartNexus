import time
import threading
from queue import Queue
import matplotlib.pyplot as plt

# 请求队列Q1
q = Queue()
# 每个请求被push进Q1的时刻
list1 = []
# 用来生成最后list2的
qpop = Queue()
# 检测
qjc = Queue(1)
# 检测user线程是否push完请求
qzz = Queue(1)
# 每一次Q2pop时的时刻
list2 = []
list1.append(0)
def user() :
    count = 1
    t = 0
    for i in range(2,21):
        time.sleep(0.125)
        t += 0.125
        list1.append(t)
        q.put(i)
        q.get()
        count += 1
        if count%4==0:
            qpop.put(list1[i-1])
            qjc.put(1)
        print('request{} pushed'.format(i))
    qzz.put(1)

def gg():
    while qzz.empty():
        if qjc.full():
            qjc.get()
            time.sleep(0.5)
            temp = qpop.get()
            temp += 0.5
            for a in range(4):
                list2.append(temp)
            print('requests processed')
    for i in range(20):
        list2[i] = 1000*(list2[i] - list1[i])
    print("latency(ms) for each request:")
    print(list2)
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    y = [list2[index] for index in range(20)]
    # 绘制图形
    plt.plot(x, y, linewidth=1, color="blue", marker="*", label="Latency")
    plt.xlabel("Request ID")
    plt.ylabel("Latency(ms)")
    plt.xticks([5, 10, 15, 20])
    plt.yticks([500, 550, 600, 650, 700, 750, 800, 850])
    plt.show()

thread1 = threading.Thread(target=user)
thread1.start()
# thread2 = threading.Thread(target=gg)
# thread2.start()
gg()