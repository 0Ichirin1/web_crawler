# -*- coding:utf-8 -*-
# 多线程抓取 糗事百科 段子
import requests
from lxml import etree
import time
import sys
from fake_useragent import UserAgent
from requests.sessions import HTTPAdapter
from queue import Queue
from threading import Thread

ua = UserAgent()
# 请求头
headers = {
    'accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8',
    'user-agent':ua.random
}

class CrawlInfo(Thread):
    def __init__(self, url_queue, html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue

    def run(self):
        while self.url_queue.empty() == False:
            url = self.url_queue.get()
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                self.html_queue.put(res.text)

class ParseInfo(Thread):
    def __init__(self, html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue

    def run(self):
        while self.html_queue.empty() == False:
            e = etree.HTML(self.html_queue.get())
            span_text = e.xpath("//a[@class='contentHerf']/div[@class='content']/span[1]")
            with open("dz.txt", "a", encoding="utf-8") as f:
                for span in span_text:
                    info = span.xpath("string(.)")  # string(.)关键字获取所有文本信息
                    f.write(info)

if __name__ == "__main__":
    start = time.time()

    url_queue = Queue()
    html_queue = Queue()

    base_url = "https://www.qiushibaike.com/text/page/{}"
    for i in range(1, 14):
        print("正在爬取{}页".format(i))
        new_url = base_url.format(i)
        url_queue.put(new_url)

    crawl_list = []
    for i in range(3):
        Crawl = CrawlInfo(url_queue, html_queue)
        crawl_list.append(Crawl)
        Crawl.start()

    for crawl in crawl_list:
        crawl.join()

    parse_list = []
    for i in range(3):
        Parse = ParseInfo(html_queue)
        parse_list.append(Parse)
        Parse.start()

    for parse in parse_list:
        parse.join()

    end = time.time()
    print(end-start)




