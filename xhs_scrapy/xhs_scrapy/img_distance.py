# -*- coding: utf-8 -*-
from io import BytesIO
import numpy as np
import cv2
import requests
from PIL import Image

from .track import slide_track


class SlideCrack(object):
    def __init__(self, gap, bg, out=None):
        """
        init code
        :param gap: 缺口图片
        :param bg: 背景图片
        :param out: 输出图片
        """
        self.gap = gap
        self.bg = bg
        self.out = out

    @staticmethod
    def clear_white(img):
        # 清除图片的空白区域，这里主要清除滑块的空白
        img = cv2.imdecode(np.frombuffer(requests.get(url=img,verify=False).content,np.uint8), cv2.IMREAD_UNCHANGED)
        rows, cols, channel = img.shape
        min_x = 255
        min_y = 255
        max_x = 0
        max_y = 0
        for x in range(1, rows):
            for y in range(1, cols):
                t = set(img[x, y])
                if len(t) >= 2:
                    if x <= min_x:
                        min_x = x
                    elif x >= max_x:
                        max_x = x

                    if y <= min_y:
                        min_y = y
                    elif y >= max_y:
                        max_y = y
        img1 = img[min_x:max_x, min_y: max_y]
        return img1

    def template_match(self, tpl, target):
        th, tw = tpl.shape[:2]
        result = cv2.matchTemplate(target, tpl, cv2.TM_CCOEFF_NORMED)
        # 寻找矩阵(一维数组当作向量,用Mat定义) 中最小值和最大值的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        # 绘制矩形边框，将匹配区域标注出来
        # target：目标图像
        # tl：矩形定点
        # br：矩形的宽高
        # (0,0,255)：矩形边框颜色
        # 1：矩形边框大小
        cv2.rectangle(target, tl, br, (0, 0, 255), 2)
        if self.out:
            cv2.imwrite(self.out, target)
        return tl[0]

    @staticmethod
    def image_edge_detection(img):
        edges = cv2.Canny(img, 100, 200)
        return edges

    def discern(self):
        img1 = self.clear_white(self.gap)
        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        slide = self.image_edge_detection(img1)
        # cv2.imwrite('img/2.png',slide)
        # back = cv2.imread(self.bg, 0)
        # print('\n',back.shape)
        data = Image.open(BytesIO(requests.get(url=self.bg, verify=False).content))
        back = cv2.cvtColor(np.asarray(data), cv2.COLOR_RGB2GRAY)
        back = self.image_edge_detection(back)

        slide_pic = cv2.cvtColor(slide, cv2.COLOR_GRAY2RGB)
        back_pic = cv2.cvtColor(back, cv2.COLOR_GRAY2RGB)
        x = self.template_match(slide_pic, back_pic) # 滑块偏移值
        # 输出横坐标, 即 滑块在图片上的位置
        # print(x)
        return x


if __name__ == "__main__":
    import re
    import requests,time
    import urllib3
    urllib3.disable_warnings()

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
    # while True:
    response = requests.get('https://captcha.fengkongcloud.com/ca/v1/register', headers=headers, params=params,verify=False).text

    # rid = re.compile('"rid":"(.*?)"').findall(response)[0]
    # k = re.compile('"k":"(.*?)"').findall(response)[0]

    # bg = 'https://castatic.fengkongcloud.com'+re.compile('"bg":"(.*?)"').findall(response)[0]
    # fg = 'https://castatic.fengkongcloud.com'+re.compile('"fg":"(.*?)"').findall(response)[0]
    bg = 'https://castatic.fengkongcloud.com/crb/set-20200506/v4/ffc64eafcf4c726717b870b6c4fa2040_bg.jpg'
    fg = 'https://castatic.fengkongcloud.com/crb/set-20200506/v4/ffc64eafcf4c726717b870b6c4fa2040_fg.png'
    print(bg)
    print(fg)


    sc = SlideCrack(fg,bg, "img/33.png")
    distance = int(sc.discern()//2/0.8133333333333334) #数美滑块下载的图片像素为页面上图片的两倍
    # print('缺口位置',distance)
    arr_track = slide_track.get(distance) or slide_track.get(distance - 1) or slide_track.get(
        distance + 1) or slide_track.get(distance + 2) or slide_track.get(distance - 2)
    print(arr_track)
    print(distance)
    if not arr_track:
        print('缺口位置', distance)
