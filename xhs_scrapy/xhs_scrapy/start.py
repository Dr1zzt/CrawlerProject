#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   run.py
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/4/7 10:40   Drizzt      1.0         None
"""
from scrapy import cmdline

if __name__ == "__main__":
    # cmdline.execute(["scrapy", "crawl", "dy_note_comment", "-a", "task_id=5068"])
    # cmdline.execute(["scrapy", "crawl", "dy_test", "-a", "task_id=3654"])
    # cmdline.execute(["scrapy", "crawl", "dy_user_note_comment", "-a", "task_id=5084"])
    # cmdline.execute(["scrapy", "crawl", "dy_comment", "-a", "task_id=5423"])
    # cmdline.execute(["scrapy", "crawl", "dy_user", "-a", "task_id=4908"])
    # cmdline.execute(["scrapy", "crawl", "dy_author", "-a", "task_id=4877"])
    # cmdline.execute(["scrapy", "crawl", "xhs_author", "-a", "task_id=3301"])
    # cmdline.execute(["scrapy", "crawl", "dy_challenge", "-a", "task_id=5093"])
    # cmdline.execute(["scrapy", "crawl", "dy_challenge_author", "-a", "task_id=2617"])
    # cmdline.execute(["scrapy", "crawl", "dy_address", "-a", "task_id=2615"])
    cmdline.execute(["scrapy", "crawl", "xhs_note_comment", "-a", "task_id=6054"])
    # cmdline.execute(["scrapy", "crawl", "xhs_user", "-a", "task_id=4903"])
