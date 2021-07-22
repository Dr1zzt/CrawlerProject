#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   run.py    
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/5/11 17:10   Drizzt      1.0         None
"""

from scrapy import cmdline

if __name__ == "__main__":
    cmdline.execute(["scrapy", "crawl", "dy_challenge"])
