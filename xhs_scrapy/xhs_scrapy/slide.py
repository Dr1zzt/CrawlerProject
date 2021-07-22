# -*- coding: utf-8 -*-
'''
@File:      login.py
@SourceUrl:
@Author:    阿J
@Date:      2021/4/8 16:57
@Software:  PyCharm
@Desc:
'''
from subprocess import Popen, PIPE

import execjs
import re
import requests,time
from .img_distance import SlideCrack
from .track import slide_track
import urllib3
urllib3.disable_warnings()


def fengkong(authorization):
    headers = {
        'Host': 'captcha.fengkongcloud.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type': 'application/json',
        'referer': 'https://servicewechat.com/wxb296433268a1c654/22/page-frame.html',
    }

    params = (
        ('organization', 'eR46sBuqF0fdw7KWFLYa'),
        ('appId', 'default'),
        ('channel', 'miniProgram'),
        ('lang', 'zh-cn'),
        ('model', 'slide'),
        ('rversion', '1.0.1'),
        ('sdkver', '1.1.1'),
        ('data', '{}'),
        ('callback', 'sm_{}'.format(int(time.time()*1000))),
    )

    response = requests.get('https://captcha.fengkongcloud.com/ca/v1/register', headers=headers, params=params,verify=False).text

    rid = re.compile('"rid":"(.*?)"').findall(response)[0]
    k = re.compile('"k":"(.*?)"').findall(response)[0]

    bg = 'https://castatic.fengkongcloud.com'+re.compile('"bg":"(.*?)"').findall(response)[0]
    fg = 'https://castatic.fengkongcloud.com'+re.compile('"fg":"(.*?)"').findall(response)[0]


    # 获取缺口位置，并生成滑动轨迹
    # sc = SlideCrack(fg,bg,"img/33.png")
    sc = SlideCrack(fg,bg)
    distance = int(sc.discern()//2/0.8133333333333334) #数美滑块下载的图片像素为页面上图片的两倍
    print('缺口位置', distance)

    with open('./code.js', encoding='utf8') as f:
        js_func = execjs.compile(f.read())

    slide_info = slide_track.get(distance) or slide_track.get(distance - 1) or slide_track.get(distance + 1) or slide_track.get(distance + 2) or slide_track.get(distance - 2)

    # 轨迹加密
    act = js_func.call('get_sli',distance,k,slide_info)
    print(act)

    params = (
        ('organization', 'eR46sBuqF0fdw7KWFLYa'),
        ('appId', 'default'),
        ('channel', 'miniProgram'),
        ('lang', 'zh-cn'),
        ('rversion', '1.0.1'),
        ('sdkver', '1.1.1'),
        ('rid', rid),
        ('act', act),
        ('ostype', 'weapp'),
        ('data', '{}'),
        ('callback', 'sm_{}'.format(int(time.time()*1000))),
    )

    response = requests.get('https://captcha.fengkongcloud.com/ca/v1/fverify', headers=headers, params=params,verify=False)
    print(response.text)

    # 校验 必须携带小程序用户参数authorization
    headers = {
        'Host': 'www.xiaohongshu.com',
        'authorization': authorization,
        'device-fingerprint': 'WHJMrwNw1k/GpHZM63YJcdldxF4qslq9AF5SrNmQxU8exAx/Rqivx6Rw1lrvChD3miV2o9NPN7OevVeBNqqcx+gjLbOjPLIIMdCW1tldyDzmauSxIJm5Txg==1487582755342',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'x-sign': 'X013b36ebf3a70cf8a82051e3f246ab19',
        'content-type': 'application/json',
        'referer': 'https://servicewechat.com/wxb296433268a1c654/22/page-frame.html',
    }

    data = '{"rid":"'+rid+'","status":1,"callFrom":"wxMiniProgram"}'
    response = requests.post('https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/shield/captchaV2', headers=headers, data=data,verify=False)
    print(response.text)





