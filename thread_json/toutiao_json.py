from test_json.ToutiaoThread import ToutiaoThread
from test_json.SessionThread import SessionThread
import queue


if __name__ == '__main__':
    queue = queue.Queue()
    session = SessionThread(queue)
    session.start()
    for work in range(3):
        work_thread = ToutiaoThread(queue)
        work_thread.start()
    # session.join()
    # queue.join()








