#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   redisUtil.py
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/4/7 14:23   Drizzt      1.0         None
"""

import redis


class RedisConn:
    def __init__(self):
        self.host = ""
        self.port = 6379
        self.password = ""

    def connect(self):
        pool = redis.ConnectionPool(
            host=self.host,
            port=self.port,
            decode_responses=True,
            password=self.password
        )

        return redis.Redis(connection_pool=pool)
