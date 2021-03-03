# -*- coding:utf-8 -*-
#  多线程 下载 豆瓣 刘诗诗 图片
import requests
import json
import os
from selenium import webdriver
from queue import Queue
from lxml import etree
from fake_useragent import UserAgent
from threading import Thread
from time import time

ua = UserAgent()
# 请求头
headers = {
    'accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8',
    'user-agent': ua.random
}

# 爬虫类
class DownloadImage(Thread):
    def __init__(self, url_queue, html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue

    def run(self):
        while self.url_queue.empty() == False:
            url = self.url_queue.get()
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                self.html_queue.put(res.text)
            else:
                print("请求失败")

# 解析类
class ParseInfo(Thread):
    def __init__(self, html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue

    def run(self):
        while self.html_queue.empty() == False:
            html = self.html_queue.get()
            formatting_pages = etree.HTML(html)
            images = formatting_pages.xpath(
                "//ul[@class='poster-col3 clearfix']/li/div[@class='cover']/a/img/@src")

            pic_path = "shishi"
            if not os.path.exists(pic_path):
                os.makedirs(pic_path)

            base_path = os.getcwd() + "/" + pic_path + "/"

            for image in images:
                dir_name = base_path + image.split("/")[-1].split(".")[0] + ".jpg"
                try:
                    pic = requests.get(image, timeout=15, headers=headers)
                    with open(dir_name, "wb") as f:
                        f.write(pic.content)
                except requests.exceptions.ConnectionError:
                    print("连接失败，图片无法下载")


if __name__ == '__main__':
    start_time = time()

    url_queue = Queue()
    html_queue = Queue()

    for i in range(0, 2791, 30):
        url = "https://movie.douban.com/celebrity/1274533/photos/?type=C&start={}&sortby=like&size=a&subtype=a".format(str(i))
        url_queue.put(url)

    crawl_list = []
    for _ in range(6):
        crawl_obj = DownloadImage(url_queue, html_queue)
        crawl_list.append(crawl_obj)
        crawl_obj.start()

    for crawl in crawl_list:
        crawl.join()

    parse_list = []
    for _ in range(6):
        parse_obj = ParseInfo(html_queue)
        parse_obj.start()
        parse_list.append(parse_obj)

    for parse in parse_list:
        parse.join()

    end_time = time()
    print(end_time-start_time)