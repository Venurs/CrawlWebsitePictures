from urllib import request, parse, error
import re
import time

#  模拟浏览器
header = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/57.0")
opener = request.build_opener()

opener.addheaders = [header]
request.install_opener(opener)  # 将opener安装为全局

article_list = []  # 文章列表，用于存储每一页的文章链接


#  使用代理服务器
def use_proxy(proxy_addr, url):
    """

    :param proxy_addr: 代理服务器的地址
    :param url: 待爬取的URL
    :return: 返回链接爬到的数据
    """
    try:
        proxy = request.ProxyHandler({"http": proxy_addr})
        opener = request.build_opener(proxy, request.ProxyHandler)
        request.install_opener(opener)
        data = request.urlopen(url=url).read().decode("utf-8")
        return data
    except error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        print(use_proxy.__doc__)
        time.sleep(5)
    except Exception as e:
        print("exception" + str(e))
        print(use_proxy.__doc__)
        time.sleep(2)


def get_articles(key, pagestart, pageend, proxy_addr):
    """

    :param key: url中的关键字:python+爬虫(只需要将爬虫进行二进制编码)
    :param pagestart: 搜索到的文章的开始页为1
    :param pageend: 搜索到的文章的结束页为10
    :param proxy_addr: 代理服务器地址
    :return: 返回搜索的文章的链接地址
    """
    try:
        key = request.quote(key)
        for page in range(pagestart, pageend + 1):
            url = "http://weixin.sogou.com/weixin?query=" + str(key) + "&type=2&page=" + str(page)
            data = use_proxy(proxy_addr, url)
            reg = '<target="_blank" href="?(http://mp.weixin.qq.com/s?src=11.*)"'
            article_list.append(re.compile(reg, ).findall(data))
        print("article的长度为：", len(article_list))
        return article_list
    except error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        print(get_articles.__doc__)
        time.sleep(5)
    except Exception as e:
        print("exception" + str(e))
        print(get_articles.__doc__)
        time.sleep(2)


def get_content(proxy_addr, article_list):
    """
    获取文章链接下的文章内容并保存为网页文件
    :param proxy_addr:代理服务器地址
    :param article_list: 存储文章链接的列表(连接中含有待处理项)
    :return:
    """
    try:
        #  网页头部
        html = "<!DOCTYPE html><html><head><title>微信文章网页</title></head><body>"
        #  i为页码，j为对应页的第几篇文章
        for i in range(0, len(article_list)):
            for j in range(0, len(i)):
                # 处理拿到的链接，将其中的"amp;"去除掉
                url = article_list[i][j]
                url = url.replace("amp;", "")
                data = use_proxy(proxy_addr, url)
                reg_title = r'<h2 class="rich_media_title" id="activity-name">?(.*)</h2>'
                reg_content = '<div class="rich_media_content " id="js_content">?(.*)</div>'
                title = re.findall(re.compile(reg_title), data)
                content = re.findall(re.compile(reg_content), data)
                path = "source/"+"页码" + i + "/" + title[0] + ".html"
                file = open(path, mode="wb")
                file.write(html.encode("utf-8"))
                file.close()
                file = open(path, mode="ab")
                thistitle = "空标题"
                thiscontent = "空内容"
                if len(reg_title) != 0:
                    thistitle = reg_title[0]
                if len(reg_content) != 0:
                    thiscontent = reg_content[0]
                html_content = "<p>标题是" + thistitle + "</p><p>内容为：" + "</p></body></html>"
                file.write(html_content.encode("utf-8"))
                file.close()
    except error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        print(get_content.__doc__)
        time.sleep(5)
    except Exception as e:
        print("exception:" + str(e))
        print(get_content.__doc__)
        time.sleep(2)

if __name__ == '__main__':













