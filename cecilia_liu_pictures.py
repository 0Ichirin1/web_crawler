# -*- coding:utf-8 -*-
#  多线程 下载 豆瓣 刘诗诗 图片
import requests
import json
import os
import random
from selenium import webdriver
from queue import Queue
from lxml import etree
from fake_useragent import UserAgent
from threading import Thread
from time import time, sleep

PIC_PATH = "shishi"
ua = UserAgent()
# 请求头
headers = {
    'accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8',
    'user-agent': ua.random
}

# 爬虫类
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
                sleep_time = random.randint(0, 2) + random.random()
                sleep(sleep_time)
            else:
                print("请求失败,{}".format(str(res.status_code)))

# 解析图片列表类
class ParseImageList(Thread):
    def __init__(self, url_queue, html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue

    def run(self):
        while self.html_queue.empty() == False:
            html = self.html_queue.get()
            formatting_pages = etree.HTML(html)
            images = formatting_pages.xpath(
                "//ul[@class='poster-col3 clearfix']/li/div[@class='cover']/a/img/@src")

            for image in images:
                self.url_queue.put(image)


def crawl_func(url_q, html_q):
    crawl_list = []
    for _ in range(6):
        crawl_obj = CrawlInfo(url_q, html_q)
        crawl_list.append(crawl_obj)
        crawl_obj.start()

    for crawl in crawl_list:
        crawl.join()

def parse_func(url_q, html_q):
    parse_list = []
    for _ in range(6):
        parse_obj = ParseImageList(url_q, html_q)
        parse_obj.start()
        parse_list.append(parse_obj)

    for parse in parse_list:
        parse.join()

# 下载图片
def download_info(image):
    dir_name = base_path + image.split("/")[-1].split(".")[0] + ".jpg"
    try:
        pic = requests.get(image, timeout=12, headers=headers)
        with open(dir_name, "wb") as f:
            f.write(pic.content)
    except requests.exceptions.ConnectionError:
        print("连接失败，图片无法下载")

if __name__ == '__main__':
    start_time = time()

    # 声明 存放url的队列 和 html源码的队列
    url_queue = Queue()
    html_queue = Queue()

    # 创建存放图片的文件夹 exist_ok=True 表示如果文件夹已存在，就什么都不做
    os.makedirs(PIC_PATH, exist_ok=True)
    base_path = os.getcwd() + "/" + PIC_PATH + "/"
    # 将 图片列表的url添加到url队列中去
    for i in range(0, 2791, 30):
        url = "https://movie.douban.com/celebrity/1274533/photos/?type=C&start={}&sortby=like&size=a&subtype=a".format(str(i))
        url_queue.put(url)

    crawl_func(url_queue, html_queue)
    parse_func(url_queue, html_queue)
    for image in url_queue.get():
        print(image)
        download_info(image)

    end_time = time()
    print(end_time-start_time)

