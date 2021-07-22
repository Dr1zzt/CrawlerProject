#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   decryptUtil.py    
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/5/21 9:10   Drizzt      1.0         None
"""
import hashlib
from urllib import parse

import frida


call_back_message = ""


def md5(code):
    return hashlib.md5(code.encode("utf-8")).hexdigest()


def on_message(message, data):  # js中执行send函数后要回调的函数
    global call_back_message
    if message["type"] == "send":
        call_back_message = message['payload']


def get_x_ss_stub(data):
    result = "&".join([f"{i}={parse.quote(j)}" for i, j in data.items()])
    return md5(result).upper()


def get_x_gorgon(url, cookie, x_khronos, is_post=False, x_ss_stub=None):
    if is_post:
        str4 = x_ss_stub
    else:
        str4 = "0" * 32
    a2 = md5(parse.urlparse(url).query)
    str5 = md5(cookie)
    str6 = "0" * 32
    data = a2 + str4 + str5 + str6
    jscode = 'function Str2BytesObj(str){var pos = 0;var len = str.length;if(len %2 != 0){return null;}len /= 2;var ObjA = new Object();for(var i=0; i<len; i++){var s = str.substr(pos, 2);var v = parseInt(s, 16);if(v >127) v = v-255-1;ObjA[i] = v;pos += 2;}ObjA[\'length\'] = len;return ObjA;};rpc.exports = {gethello: function(str){Java.perform(function(){var ByteString = Java.use("com.android.okhttp.okio.ByteString");var AuthUtils = Java.use(\'com.ss.sys.ces.a\');var a = -1;var timestamp = Date.parse(new Date())/ 1000;var b = ' + str(
        int(x_khronos)) + ';var c = \'' + data + '\';c = Str2BytesObj(c);var sig = AuthUtils.leviathan(a,b,c);send(ByteString.of(sig).hex());})}};'
    str_host = '172.16.0.25:6666'
    manager = frida.get_device_manager()
    remote_device = manager.add_remote_device(str_host)
    process = remote_device.attach('com.ss.android.ugc.aweme')
    script = process.create_script(jscode)
    script.on('message', on_message)
    script.load()
    script.exports.gethello()
    return call_back_message
