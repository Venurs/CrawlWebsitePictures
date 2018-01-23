from test_json.database import MysqlHelple
from threading import Thread
import datetime
import requests


class ToutiaoThread(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.mysql = MysqlHelple(host="localhost", user="root", password="39861711", db="toutiao")
        self.connect, self.cursor = self.mysql.connect()
        self.download_session = requests.Session()

    def run(self):
        while True:
            # try:
            data = self.queue.get()
            #  执行数据库插入操作
            print("队列取出数据：", data)
            # print("队列去除数据成功")

            # 插入新闻到t_news表
            params = ToutiaoThread.news_data_hander(data)
            self.mysql.insert_into_t_news(self.connect, self.cursor, params)
            #  下载图片
            ToutiaoThread.save_image(data=data, session=self.download_session)
            #  插入新闻的label到t_label表
            labels = data.get("label", [])
            print(labels)
            if labels:
                for label in labels:
                    print(label)
                    label_id = self.mysql.select_label_id(self.connect, self.cursor, label)
                    print(label_id)
                    param = []
                    param.append(data.get("item_id", None))
                    param.append(label_id)
                    params = tuple(param)
                    self.mysql.insert_into_t_news_label(self.connect, self.cursor, params)
            else:
                print("无label属性")
            # except Exception as e:
            #     print("线程%s出现错误%s" % (self.getName(), e))

    @staticmethod
    def news_data_hander(data):
        param = []
        param.append(str(datetime.datetime.now().timestamp()))
        param.append(data.get("item_id", None))
        param.append(data.get("tag", None))
        param.append(data.get("chinese_tag", None))
        param.append(data.get("title", None))
        param.append(data.get("abstract", None))
        param.append(data.get("media_url", None))
        params = tuple(param)
        return params

    @staticmethod
    def download_image(session, url):
        header = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
            "Cookie": 'uuid="w:c8d478c6374349e28b087f324c1e9f86"; UM_distinctid=160f49c67d3158-075946cf74f123-c303767-1fa400-160f49c67d633; _ga=GA1.2.1587432095.1515932379; _gid=GA1.2.474240878.1515932379; CNZZDATA1259612802=1726415142-1515928137-%7C1515928137; __tasessionId=2ayv5rzn01515932611457; tt_webid=6510879981500499460; tt_webid=6510879981500499460; WEATHER_CITY=%E5%8C%97%E4%BA%AC'
        }
        url = "http:" + url
        requ = session.get(url=url)
        suffix = requ.headers["Content-Type"]
        img, suffix = str(suffix).split("/")
        file = open("img/"+str(datetime.datetime.now().timestamp()) + "." + suffix,  mode="bw")
        file.write(requ.content)
        print("图片下载成功")
        file.close()

    @staticmethod
    def save_image(data, session):
        urls = data.get("image_list")
        print(urls)
        if urls:
            for url in urls:
                ToutiaoThread.download_image(session=session, url=url.get("url"))
        else:
            print("无image_list属性")









