# -*- coding:utf-8 -*-
#  乐视电影评论 mongoDB
import re
import json
import requests
from pymongo import MongoClient
from fake_useragent import UserAgent

UA = UserAgent()
client = MongoClient()
database = client["letv"]
col = database["comments"]

class letvSpider(object):
    COMMENT_URL = "http://api-my.le.com/vcm/api/list?jsonp=jQuery191034898677137438994_1614920984314\
                &type=video&rows=20&page={}&sort=&cid=1&source=1&xid={}&pid={}&ctype=cmt%2Cimg%2Cvote&listType=1&_=1614920984324"

    HEADERS = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "tj_lc=dbd57095c40f39c8d879835d4d1f551b; tj_uuid=-_16149134837098159003; tj_env=1; bd_xid=dbd57095c40f39c8d879835d4d1f551b; ssoCookieSynced=1; ark_uuid=ck-c18ec43a-1321-4aca-a87e-5646d40b476b-0305-110624; tj_v2c=-22284564_1; currentLeft_miniPlayer=945; currentTop_miniPlayer=89",
        "DNT": "1",
        "Host": "api-my.le.com",
        "Pragma": "no-cache",
        "Referer": "http://www.le.com/",
        "User-Agent": UA.random,
    }

    def __init__(self, url):
        self.necessary_info = {}
        self.url = url
        self.get_necessary_id()
        self.get_comment()

    def get_source(self, url, headers):
        return requests.get(url, headers).content.decode()

    def get_necessary_id(self):
        source = self.get_source(self.url, self.HEADERS)
        vid = re.search("vid: (\d+)", source).group(1)
        pid = re.search("pid: (\d+)", source).group(1)
        self.necessary_info["xid"] = vid
        self.necessary_info["pid"] = pid

    def get_comment(self):
        urls = [self.COMMENT_URL.format(str(i), self.necessary_info['xid'], self.necessary_info['pid']) for i in range(1, 36)]
        for url in urls:
            source = self.get_source(url, self.HEADERS)
            source_json = source[source.find('{"'): -1]
            comment_dict = json.loads(source_json)
            comments = comment_dict["data"]
            for comment in comments:
                print(f"发帖人: {comment['user']['username']}, 评论内容: {comment['content']}")
                col.insert(comment)

if __name__ == '__main__':
    spider = letvSpider("http://www.le.com/ptv/vplay/22284564.html")

