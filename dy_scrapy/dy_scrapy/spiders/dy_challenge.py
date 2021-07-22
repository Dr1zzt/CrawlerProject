#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   dy_note_comment.py    
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/5/11 15:25   Drizzt      1.0         None
"""

# -*- coding: utf-8 -*-
import random
import json
import time

from scrapy import signals
import signal
from pydispatch import dispatcher
from scrapy.signalmanager import SignalManager
from scrapy import FormRequest

from ..items import DyNoteItem, DyCommentItem
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from ..common.decryptUtil import get_x_ss_stub, get_x_gorgon


class DyChallengeSpider(CrawlSpider):
    name = 'dy_challenge'
    SEARCH_URL = "https://search3-search-hl.amemv.com/aweme/v1/challenge/search/?_rticket={}&oaid=f58d06137f822b09&" \
                 "ts={}&"

    CHALLENGE_URL = "https://api5-normal-c-hl.amemv.com/aweme/v1/challenge/aweme/?cursor={}&ch_id={}&" \
                    "mac_address=A4%3A50%3A46%3AEE%3A65%3ADC&count={}&query_type=0&source=challenge_video&" \
                    "type=5&_rticket={}&oaid=f58d06137f822b09&ts={}&"

    COMMENT_URL = "https://api3-normal-c-hl.amemv.com/aweme/v2/comment/list/?aweme_id={}&cursor={}&count=20&" \
                  "address_book_access=2&gps_access=1&forward_page_type=1&channel_id=0&city=450100&hotsoon_filtered_count=0&" \
                  "hotsoon_has_more=0&manifest_version_code=100201&_rticket={}&app_type=normal&iid=1091167479145496&" \
                  "channel=tengxun_new&device_type=MI%208&language=zh&resolution=1080*2028&openudid=46558cf97da0db50&" \
                  "update_version_code=10209900&cdid=5a04639f-d032-416b-ac9d-472e6bc647e9&os_api=28&dpi=440&" \
                  "oaid=f58d06137f822b09&ac=wifi&device_id=66414359502&os_version=9&version_code=100200&app_name=aweme&" \
                  "version_name=10.2.0&device_brand=Xiaomi&ssmix=a&device_platform=android&aid=1128&ts={}"
    COOKIE = "odin_tt=ca21bd5115d0cc8333b842e4b5a7b07c34deddfd3aaf79d4a5c2abf39c24e3adf7b48f8e0c8297b274dee219cbe7e1222cd1688fc8d67796c0770acc387bc09b"

    def sleep(self, s=3, e=5):
        time.sleep(random.randint(s, e))

    def __init__(self, page=1, page_size=20, task_id="", *args, **kwargs):
        super(DyChallengeSpider, self).__init__(*args, **kwargs)
        SignalManager(dispatcher.Any).connect(self.closed_handler, signal=signals.spider_closed)
        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)
        self.num = 0
        self.note_page_size = 20
        self.comment_page_size = 100
        self.page = 0
        self.search_word = "LOL"

    def closed_handler(self, spider):
        pass

    def exit_handler(self, signum, frame):
        self.crawler.engine.close_spider(self, '用户主动停止爬虫!')

    def start_requests(self):
        user_page = 1
        user_page_size = 20
        send_time = int(time.time() * 1000)
        x_khronos = send_time / 1000
        _rticket = send_time + random.randint(2, 8)
        url = self.SEARCH_URL.format(_rticket, int(x_khronos))
        x_common_params_v2 = "os_api=28&device_platform=android&device_type=MI%208&iid=1091167479145496&version_code=100200&app_name=aweme&openudid=46558cf97da0db50&device_id=66414359502&os_version=9&aid=1128&channel=tengxun_new&ssmix=a&manifest_version_code=100201&dpi=440&cdid=0e8f6b03-a655-4321-a424-1661e932d6cd&version_name=10.2.0&resolution=1080*2028&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=10209900&uuid=861997049894178"
        data = {
            'cursor': "0",
            'keyword': self.search_word,
            'count': str(user_page_size),
            'hot_search': '0',
            'is_pull_refresh': '1',
            'search_source': 'challenge',
            'search_id': '',
            'query_correct_type': '1'
        }
        headers = {
            "x-ss-req-ticket": str(send_time),
            "x-tt-token": "00368efa7dc537dd49d46533861ce19b0b027b7d4521842969a47687c69f48f72a1125236f37a10980a612253f74579947b3d81e365d16db71d12545b8370e3b6fb0dfa5d95406e9a5660f1984f8f3e2dcfea497f1dfd844b41703cdb2637d130b05a",
            "sdk-version": "1",
            "x-ss-stub": get_x_ss_stub(data),
            "x-ss-dp": "1128",
            "user-agent": "com.ss.android.ugc.aweme/100201 (Linux; U; Android 9; zh_CN; MI 8; Build/PKQ1.180729.001; Cronet/TTNetVersion:79d23018 2020-02-03 QuicVersion:ac58aac6 2020-01-20)",
            "accept-encoding": "gzip, deflate",
            "x-khronos": str(int(x_khronos)),
            "x-gorgon": get_x_gorgon(url+x_common_params_v2, self.COOKIE, x_khronos, is_post=True,
                                     x_ss_stub=get_x_ss_stub(data)),
            "x-common-params-v2": "os_api=28&device_platform=android&device_type=MI%208&iid=1091167479145496&version_code=100200&app_name=aweme&openudid=46558cf97da0db50&device_id=66414359502&os_version=9&aid=1128&channel=tengxun_new&ssmix=a&manifest_version_code=100201&dpi=440&cdid=0e8f6b03-a655-4321-a424-1661e932d6cd&version_name=10.2.0&resolution=1080*2028&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=10209900&uuid=861997049894178",
            "cookie": self.COOKIE
        }
        yield FormRequest(url=url, headers=headers, formdata=data, callback=self.parse_challenge,
                          meta={"note_id": self.search_word, "user_page": user_page})

    def parse_challenge(self, response):
        # 因为每个话题下面的视频太多，暂时只获取话题页的第一页
        data = json.loads(response.text)
        items = data["challenge_list"]
        if items:
            for item in items:
                item = item["challenge_info"]
                cha_id = item["cid"]
                challenge_page_size = 20

                send_time = int(time.time() * 1000)
                x_khronos = int(send_time / 1000)
                _rticket = send_time + random.randint(2, 8)
                url = self.CHALLENGE_URL.format(challenge_page_size*(self.page-1), cha_id, challenge_page_size,
                                                _rticket, x_khronos)
                x_common_params_v2 = "os_api=28&device_platform=android&device_type=MI%208&iid=1091167479145496&version_code=100200&app_name=aweme&openudid=46558cf97da0db50&device_id=66414359502&os_version=9&aid=1128&channel=tengxun_new&ssmix=a&manifest_version_code=100201&dpi=440&cdid=0e8f6b03-a655-4321-a424-1661e932d6cd&version_name=10.2.0&resolution=1080*2028&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=10209900&uuid=861997049894178"
                headers = {
                    "x-ss-req-ticket": str(_rticket),
                    "x-tt-token": "00f7fb085e934da5bfea3fc01447821c85037e5333df3bd7d260d74380ef083876c0ce9373a0b7456c7bd202fcc97c672dafc9cc065f7d6f10d5a750631253494131df10ba41d5f845492f7a5776b4508e65c5e80c6132360352311501bc4b9df2e4f-1.0.1",
                    "sdk-version": "1",
                    "x-ss-dp": "1128",
                    "user-agent": "com.ss.android.ugc.aweme/100201 (Linux; U; Android 9; zh_CN; MI 8; Build/PKQ1.180729.001; Cronet/TTNetVersion:79d23018 2020-02-03 QuicVersion:ac58aac6 2020-01-20)",
                    "accept-encoding": "gzip, deflate",
                    "x-khronos": str(int(x_khronos)),
                    "x-common-params-v2": "os_api=28&device_platform=android&device_type=MI%208&iid=1091167479145496&version_code=100200&app_name=aweme&openudid=46558cf97da0db50&device_id=66414359502&os_version=9&aid=1128&channel=tengxun_new&ssmix=a&manifest_version_code=100201&dpi=440&cdid=0e8f6b03-a655-4321-a424-1661e932d6cd&version_name=10.2.0&resolution=1080*2028&language=zh&device_brand=Xiaomi&app_type=normal&ac=wifi&update_version_code=10209900&uuid=861997049894178",
                    "x-gorgon": get_x_gorgon(url + x_common_params_v2, self.COOKIE, x_khronos),
                    "cookie": self.COOKIE
                }
                yield Request(url=url, headers=headers, callback=self.parse_note, meta={"note_page": self.page})

    def parse_note(self, response):
        # 因为每个话题下面的视频太多，暂时只获取视频页的第一页
        comment_page = 1
        comment_page_size = 20
        data = json.loads(response.text)
        note_page = response.meta["note_page"]
        items = data["aweme_list"]
        for item in items:
            note_item = DyNoteItem()
            note_item["author_nickname"] = item["author"]["nickname"]
            note_item["aweme_id"] = item["aweme_id"]
            note_item["desc"] = item["desc"]
            note_item["author_uid"] = item["author"]["uid"]
            note_item["author_short_id"] = item["author"]["short_id"]
            note_item["author_gender"] = item["author"]["gender"]
            note_item["author_unique_id"] = item["author"]["unique_id"]
            note_item["author_signature"] = item["author"]["signature"]
            note_item["note_page"] = note_page
            yield note_item

            send_time = int(time.time() * 1000)
            x_khronos = send_time / 1000
            _rticket = send_time + random.randint(2, 8)
            url = self.COMMENT_URL.format(item["aweme_id"], str(comment_page_size * (comment_page - 1)), _rticket,
                                          x_khronos)
            headers = {
                "host": "api3-normal-c-hl.amemv.com",
                "x-ss-req-ticket": str(send_time),
                "x-tt-token": "00368efa7dc537dd49d46533861ce19b0b027b7d4521842969a47687c69f48f72a1125236f37a10980a612253f74579947b3d81e365d16db71d12545b8370e3b6fb0dfa5d95406e9a5660f1984f8f3e2dcfea497f1dfd844b41703cdb2637d130b05a",
                "sdk-version": "1",
                "x-ss-dp": "1128",
                "user-agent": "com.ss.android.ugc.aweme/100201 (Linux; U; Android 9; zh_CN; MI 8; Build/PKQ1.180729.001; Cronet/TTNetVersion:79d23018 2020-02-03 QuicVersion:ac58aac6 2020-01-20)",
                "accept-encoding": "gzip, deflate",
                "x-khronos": str(int(x_khronos)),
                "x-gorgon": get_x_gorgon(url, self.COOKIE, x_khronos),
                "cookie": self.COOKIE
            }
            yield Request(url, headers=headers, callback=self.parse_comment,
                          meta={"note_id": item["aweme_id"], "comment_page": comment_page, "note_page": note_page})

    def parse_comment(self, response):
        data = json.loads(response.text)
        note_id = response.meta["note_id"]
        note_page = response.meta["note_page"]
        items = data["comments"]
        comment_page = response.meta["comment_page"]
        comment_page_size = 20
        if items:
            for item in items:
                comment_item = DyCommentItem()
                comment_item["note_id"] = note_id
                comment_item["aweme_id"] = item["aweme_id"]
                # 发布时间过滤
                comment_item["create_time"] = item["create_time"]
                comment_item["comment"] = item["text"]
                comment_item["comment"] = item["text"]
                comment_item["uid"] = item["user"]["uid"]
                comment_item["short_id"] = item["user"]["short_id"]
                comment_item["gender"] = item["user"]["gender"]
                comment_item["note_page"] = note_page
                comment_item["unique_id"] = item["user"]["unique_id"]
                yield comment_item

            comment_page += 1
            send_time = int(time.time() * 1000)
            x_khronos = send_time / 1000
            _rticket = send_time + random.randint(2, 8)
            url = self.COMMENT_URL.format(note_id, str(comment_page_size * (comment_page - 1)), _rticket, x_khronos)
            headers = {
                "host": "api3-normal-c-hl.amemv.com",
                "x-ss-req-ticket": str(send_time),
                "x-tt-token": "00368efa7dc537dd49d46533861ce19b0b027b7d4521842969a47687c69f48f72a1125236f37a10980a612253f74579947b3d81e365d16db71d12545b8370e3b6fb0dfa5d95406e9a5660f1984f8f3e2dcfea497f1dfd844b41703cdb2637d130b05a",
                "sdk-version": "1",
                "x-ss-dp": "1128",
                "user-agent": "com.ss.android.ugc.aweme/100201 (Linux; U; Android 9; zh_CN; MI 8; Build/PKQ1.180729.001; Cronet/TTNetVersion:79d23018 2020-02-03 QuicVersion:ac58aac6 2020-01-20)",
                "accept-encoding": "gzip, deflate",
                "x-khronos": str(int(x_khronos)),
                "x-gorgon": get_x_gorgon(url, self.COOKIE, x_khronos),
                "cookie": self.COOKIE
            }
            yield Request(url, headers=headers, callback=self.parse_comment,
                          meta={"note_id": note_id, "comment_page": comment_page, "note_page": note_page})


