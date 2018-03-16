#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : headImage.py
@Author: taoyx
@Contact : taoyouxian@ruc.edu.cn 
@Date  : 2018/3/14 19:15
@Desc  : 
'''
import itchat
import matplotlib.pyplot as plt
import time
import os
import TencentYoutuyun
import numpy as np
from PIL import Image
from matplotlib.font_manager import FontProperties
from wordcloud import WordCloud

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)


class FaceAPI:
    def __init__(self):
        self.appid = '10122800'  # 你的appid
        self.secret_id = 'AKIDFONCpHfiQ0PdfWJpXEKUaWGtWyZ1IENV'  # 你的secret_id
        self.secret_key = 'X7e1CC0i1ALZqw2NYuBTo5B8kHeppeHo'  # 你的secret_key
        self.userid = 'test'  # 任意字符串
        self.end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT
        self.youtu = TencentYoutuyun.YouTu(self.appid, self.secret_id, self.secret_key, self.userid, self.end_point)

    def detectFace(self, imgFile):
        res = self.youtu.DetectFace(imgFile)
        if res['errorcode'] is 0:
            return True
        else:
            return False

    def extractTags(self, imgFile):
        return self.youtu.imagetag(imgFile)  # 调用图像标签接口


def analyseHeadImage(friends):
    # Init Path
    basePath = os.path.abspath('.')
    baseFolder = basePath + '\\HeadImages\\'
    if (os.path.exists(baseFolder) == False):
        os.makedirs(baseFolder)
    # Analyse Images
    faceApi = FaceAPI()
    use_face = 0
    not_use_face = 0
    image_tags = ''
    for index in range(1, len(friends)):
        friend = friends[index]
        # Save HeadImages
        imgFile = baseFolder + 'Image%s.jpg' % str(index)
        imgData = itchat.get_head_img(userName=friend['UserName'])
        if (os.path.exists(imgFile) == False):
            with open(imgFile, 'wb') as file:
                file.write(imgData)
        # Detect Faces
        time.sleep(1)
        result = faceApi.detectFace(imgFile)
        if result is True:
            use_face += 1
        else:
            not_use_face += 1
        # Extract Tags
        result = faceApi.extractTags(imgFile)
        image_tags += (",".join(list(map(lambda x: x['tag_name'], result['tags']))) + ',')  # 将标签文件连接到一起
    labels = [u'使用人脸头像', u'不使用人脸头像']
    counts = [use_face, not_use_face]
    colors = ['red', 'yellowgreen', 'lightskyblue']
    plt.figure(figsize=(8, 5), dpi=80)
    plt.axes(aspect=1)
    plt.pie(counts,  # 性别统计结果
            labels=labels,  # 性别展示标签
            colors=colors,  # 饼图区域配色
            labeldistance=1.1,  # 标签距离圆点距离
            autopct='%3.1f%%',  # 饼图区域文本格式
            shadow=False,  # 饼图是否显示阴影
            startangle=90,  # 饼图起始角度
            pctdistance=0.6  # 饼图区域文本距离圆点距离
            )
    plt.legend(loc='upper right')
    plt.title(u'%s的微信好友使用人脸头像情况' % friends[0]['NickName'], fontproperties=font_set)
    plt.show()
    image_tags = image_tags.encode('iso8859-1').decode('utf-8')
    back_coloring = np.array(Image.open('face.jpg'))
    wordcloud = WordCloud(
        font_path='simfang.ttf',
        background_color="white",
        max_words=1200,
        mask=back_coloring,
        max_font_size=75,
        random_state=45,
        width=800,
        height=480,
        margin=15
    )
    wordcloud.generate(image_tags)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
