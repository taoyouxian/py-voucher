#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : TestImg.py
@Author: taoyx
@Contact : taoyouxian@ruc.edu.cn 
@Date  : 2018/3/16 20:24
@Desc  : 
'''
import TencentYoutuyun

from wechat.headImage import FaceAPI

appid = '10122800'  # 你的appid
secret_id = 'AKIDFONCpHfiQ0PdfWJpXEKUaWGtWyZ1IENV'  # 你的secret_id
secret_key = 'X7e1CC0i1ALZqw2NYuBTo5B8kHeppeHo'  # 你的secret_key
userid = 'test'  # 任意字符串
end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT
youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, userid, end_point)

faceApi = FaceAPI()
# ret = faceApi.detectFace("H:\\MyProject\\Pictures\\SIYU\\1010_9.jpg")
# print(ret)
# ret = faceApi.detectFace("H:\\MyProject\\Pictures\\SIYU\\1007_1.jpg")
# print(ret)
# ret = youtu.FaceCompare('H:\\MyProject\\Pictures\\SIYU\\1010_9.jpg', 'H:\\MyProject\\Pictures\\SIYU\\1010_10.jpg')
# result = youtu.DetectFace("H:\\MyProject\\Pictures\\SIYU\\1010_9.jpg")
result = faceApi.extractTags("H:\\MyProject\\Pictures\\SIYU\\1010_9.jpg")
# result = youtu.imagetag("H:\\MyProject\\Pictures\\SIYU\\1010_9.jpg")  # 调用图像标签接口
print(result)
image_tags = ''
image_tags += (",".join(list(map(lambda x: x['tag_name'], result['tags']))) + ',')  # 将标签文件连接到一起
print(image_tags)
# print(result['face'])
# if result['face']:
#     print(1)
# else:
#     print(0)
