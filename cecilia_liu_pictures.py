# -*- coding:utf-8 -*-
# 下载 豆瓣 刘诗诗 图片
import requests
import json
from selenium import webdriver
from lxml import etree
from fake_useragent import UserAgent
import os

ua = UserAgent()
# 请求头
headers = {
    'accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8',
    'user-agent': ua.random
}

def downloadImage(images):
    pic_path = "shishi"
    if not os.path.exists(pic_path):
        os.makedirs(pic_path)
    save_path = os.getcwd() + "/" + pic_path + "/"
    for image in images:
        dir = save_path + image.split("/")[-1].split(".")[0] + ".jpg"
        try:
            pic = requests.get(image, timeout=10)
            with open(dir, "wb") as f:
                f.write(pic.content)
            # fp = open(dir, "wb")
            # fp.write(pic.content)
            # fp.close()
        except requests.exceptions.ConnectionError:
            print("连接失败，图片无法下载")

if __name__ == '__main__':
    for i in range(0, 2791, 30):
        url = "https://movie.douban.com/celebrity/1274533/photos/?type=C&start={}&sortby=like&size=a&subtype=a".format(str(i))
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        images = selector.xpath("//ul[@class='poster-col3 clearfix']/li/div[@class='cover']/a/img/@src")
        downloadImage(images)

