# -*- coding: utf-8 -*-
import datetime
import random
import json
import time
import urllib
import requests
import signal

from ..items import XhsCommentItem, XhsNoteItem
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from subprocess import Popen, PIPE


SEARCH_API = "https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/search/notes?keyword={}&sortBy=general&page={}&pageSize={}&prependNoteIds=&needGifCover=true"
COMMENT_API = "https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/notes/{}/comments?pageSize={}"
COMMENT_PAGE_API = "https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/notes/{}/comments?pageSize={}&endId={}"
USER_INFO_API = "https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/user/{}?1=1"


class XhsNoteCommentSpider(CrawlSpider):
    name = 'xhs_note_comment'
    start_urls = ["https://www.xiaohongshu.com"]

    def sleep(self, s=3, e=5):
        time.sleep(random.randint(s, e))

    def __init__(self, page="1", task_id="", *args, **kwargs):
        super(XhsNoteCommentSpider, self).__init__(*args, **kwargs)
        self.num = 0
        self.page = 0
        self.note_page_size = 20
        self.comment_page_size = 100
        self.search_words = ["吴亦凡", "牙签"]
        self.authorization = "wxmp.e3ef2fc4-4941-43e9-92c1-1c18c45f1b2e"
        self.header = {
            'accept': '*/*',
            'accept-type': 'application/json',
            'authorization': self.authorization,
            'device-fingerprint': 'WHJMrwNw1k/EmoPuC7oJdbh8XpDeJ8IZLdrE68h8jXuOqDkzs3gbzPPllxif1u+nZ47Fep579nD9uR/mggFlitWvfb/wYXem+dCW1tldyDzmauSxIJm5Txg==1487582755342',
            'accept-encoding': 'br, gzip, deflate',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'accept-language': 'zh-cn'
        }
        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)

    def exit_handler(self, signum, frame):
        self.crawler.engine.close_spider(self, '用户主动停止爬虫!')

    def x_sign(self, url):
        p = Popen(["node", "x-sign.js", url], stdout=PIPE)
        return p.communicate()[0].decode().replace("\n", "")

    def get_info(self, info_url):
        self.header.update({'x-sign': self.x_sign(info_url)})
        response = requests.get(url=info_url, headers=self.header)
        data = json.loads(response.text)
        if data.get("data"):
            info = data["data"]
            return info

    def start_requests(self):
        for search_word in self.search_words:
            url = SEARCH_API.format(urllib.parse.quote(search_word), self.page, self.note_page_size)
            self.header.update({'x-sign': self.x_sign(url)})
            yield Request(url, headers=self.header, meta={"search_word": search_word, "note_page": self.page,
                                                          "authorization": self.authorization},
                          callback=self.parse_note)
            self.sleep(10, 15)

    def parse_note(self, response):
        """
        小红书列表
        :param response:
        :return:
        """
        search_word = response.meta["search_word"]
        note_page = response.meta["note_page"]
        data = json.loads(response.text)

        notes = data["data"]["notes"]
        for foobar in range(len(notes)):
            note = notes[foobar]
            note_item = XhsNoteItem()
            note_item["note_id"] = note["id"]
            note_item["note_title"] = note["title"]
            note_item["author_id"] = note["user"]["id"]
            note_item["search_word"] = search_word
            note_item["created_time"] = str(datetime.datetime.now())
            note_item["note_page"] = note_page
            self.sleep()
            info_url = USER_INFO_API.format(note_item["author_id"])
            info = self.get_info(info_url)
            note_item["author_red_id"] = info["red_id"]

            yield note_item
            comment_url = COMMENT_API.format(note_item["note_id"], self.comment_page_size)
            self.header.update({'x-sign': self.x_sign(comment_url)})
            yield Request(comment_url, method="GET", headers=self.header, meta={"note_id": note_item["note_id"],
                                                                                "note_page": note_page,
                                                                                "authorization": self.authorization},
                          callback=self.parse_comment)
            self.sleep()

        if notes:
            note_page += 1
            next_url = SEARCH_API.format(urllib.parse.quote(search_word), note_page, self.note_page_size)
            self.header.update({'x-sign': self.x_sign(next_url)})
            yield Request(next_url, meta={"note_page": note_page, "search_word": search_word,
                                          "authorization": self.authorization},
                          callback=self.parse_note, headers=self.header)

    def parse_comment(self, response):
        """
        小红书评论
        :param response:
        :return:
        """
        note_id = response.meta["note_id"]
        note_page = response.meta["note_page"]
        comments = json.loads(response.text)["data"]["comments"]
        for comment in comments:
            comment_item = XhsCommentItem()
            comment_item["content"] = comment["content"]
            comment_item["note_id"] = comment["targetNoteId"]
            comment_item["nickname"] = comment["user"]["nickname"]
            comment_item["user_id"] = comment["user"]["id"]
            comment_item["comment_time"] = comment["time"].split(" ")[0]
            comment_item["created_time"] = str(datetime.datetime.now())
            comment_item["note_page"] = note_page
            self.sleep(5, 10)
            info_url = USER_INFO_API.format(comment_item["user_id"])
            info = self.get_info(info_url)
            comment_item["xhs_id"] = info["red_id"]

            yield comment_item

        if comments:
            self.sleep()
            comment_url = COMMENT_PAGE_API.format(note_id, self.comment_page_size, comments[-1]["id"])
            self.header.update({'x-sign': self.x_sign(comment_url)})
            yield Request(comment_url, method="GET", headers=self.header,
                          meta={"note_id": note_id, "note_page": note_page, "authorization": self.authorization},
                          callback=self.parse_comment)
