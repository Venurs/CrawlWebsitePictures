"""
负责分配任务
"""
from multiprocessing.managers import BaseManager
import queue

#  新建发送任务队列和接收结果队列，每一个主机一个接收结果的队列
send_task_queue = queue.Queue()
rec_result_queue1 = queue.Queue()  # 接收爬取到的首页的链接
rec_result_queue2 = queue.Queue()
rec_result_queue3 = queue.Queue()

#  解决序列化不支持匿名函数问题


def return_send_task():
    global send_task_queue
    return send_task_queue


def return_rec_result1():
    global rec_result_queue1
    return rec_result_queue1


def return_rec_result2():
    global rec_result_queue2
    return rec_result_queue2


def return_rec_result3():
    global rec_result_queue3
    return rec_result_queue3


def master():
    #  将所有对列进行注册
    BaseManager.register("get_send_task", callable=return_send_task)
    BaseManager.register("get_result1", callable=return_rec_result1)
    BaseManager.register("get_result2", callable=return_rec_result2)
    BaseManager.register("get_result3", callable=return_rec_result3)

    #  绑定端口
    ip = ""
    port = 5000
    master = BaseManager(address=(ip, port), authkey=b"12345")






