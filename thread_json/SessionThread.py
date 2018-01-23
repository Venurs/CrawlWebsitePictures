from threading import Thread
import requests
import json
import time


class SessionThread(Thread):
    def __init__(self, queue):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
            "Cookie": 'uuid="w:c8d478c6374349e28b087f324c1e9f86"; UM_distinctid=160f49c67d3158-075946cf74f123-c303767-1fa400-160f49c67d633; _ga=GA1.2.1587432095.1515932379; _gid=GA1.2.474240878.1515932379; CNZZDATA1259612802=1726415142-1515928137-%7C1515928137; __tasessionId=2ayv5rzn01515932611457; tt_webid=6510879981500499460; tt_webid=6510879981500499460; WEATHER_CITY=%E5%8C%97%E4%BA%AC'
        }
        self.url = "https://www.toutiao.com/api/pc/feed/?min_behot_time=0&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&as=A1A5DAE54B14BDB&cp=5A5BB49BAD6B4E1&_signature=gyYLMxAc2YpijJ6ZbyGn8YMmCy"
        self.session = requests.Session()
        self.session.headers.update(headers)

        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            toutiao = self.session.get(url=self.url)
            # print(toutiao.text)
            toutiao_feed = json.loads(toutiao.text)
            for i in toutiao_feed["data"]:
                #print("队列加入：", i)
                print("队列放入数据成功")
                self.queue.put(i)
                time.sleep(10)

