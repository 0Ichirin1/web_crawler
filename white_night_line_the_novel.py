# -*- coding:utf-8 -*-
#  多线程 下载 白夜行小说 存到 MongoDB 数据库
import requests
import redis
from pymongo import MongoClient
from lxml import etree
from multiprocessing.dummy import Pool
from fake_useragent import UserAgent

ua = UserAgent()
rclient = redis.StrictRedis()
mclient = MongoClient()
novelData = mclient["novel"]
c_novel = novelData["c_novel"]
BASE_URL = "http://dongyeguiwu.zuopinj.com/5525/"
# 请求头
headers = {
    'accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8',
    'user-agent': ua.random
}

def parse_title():
    res = requests.get(BASE_URL, headers=headers)
    selector = etree.HTML(res.text)
    url_list = selector.xpath("//div[@class='book_list']/ul/li/a/@href")
    for url in url_list:
        rclient.lpush("url_queue", url)

def parse_info(url):
    source = requests.get(url, headers=headers).text.encode("iso-8859-1")
    selector = etree.HTML(source)
    title = selector.xpath("//div[@class='h1title']/h1/text()")[0]
    a_novel_text = selector.xpath("//div[@id='htmlContent']/p/text()")
    info = {"title": title, "content": "\n".join(a_novel_text)}
    return info

if __name__ == '__main__':
    parse_title()
    pool = Pool(5)
    url = []
    while rclient.llen("url_queue") > 0:
        url.append(rclient.lpop("url_queue").decode())
    info_list = pool.map(parse_info, url)
    for info in info_list:
        c_novel.insert(info_list)
