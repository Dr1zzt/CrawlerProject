#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   url_change.py    
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/18 14:37   Drizzt      1.0         None
"""

from urllib.parse import urlparse, parse_qs

info_dict = dict(iid='844889242484333', device_type='MI 8', resolution='1080*2028', openudid='46558cf97da0db50',
                 cdid='54c23e07-8a42-40d5-9bbb-bbcfbdbdb0eb', os_api='28', dpi='440', device_id='66414359502',
                 mcc_mnc='46011', os_version='9', device_brand='Xiaomi')


def url_filter(url, is_query=False):
    if not is_query:
        query = parse_qs(urlparse(url).query)
    else:
        query = parse_qs(url)
    query = {key: value[0] for key, value in query.items()}
    for key, value in info_dict.items():
        if query.get(key):
            query.pop(key)
    result = ""
    for i in query:
        result += i+"="+query[i]+"&"
    return result
