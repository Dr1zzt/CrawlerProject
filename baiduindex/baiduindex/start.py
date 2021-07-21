#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   start.py    
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/24 16:25   Drizzt      1.0         None
"""

from scrapy import cmdline

if __name__ == "__main__":
    cmdline.execute(["scrapy", "crawl", "baidu_index_crawler"])
