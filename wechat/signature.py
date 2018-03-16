#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : signature.py
@Author: taoyx
@Contact : taoyouxian@ruc.edu.cn 
@Date  : 2018/3/14 19:22
@Desc  : 
'''
import re

import jieba
import jieba.analyse
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.font_manager import FontProperties
from snownlp import SnowNLP
from wordcloud import WordCloud

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)


def analyseSignature(friends):
    signatures = ''
    emotions = []
    pattern = re.compile("1f\d.+ ")

    for friend in friends:
        signature = friend['Signature']
        if (signature != None):
            signature = signature.strip().replace('span', '').replace('class ', '').replace('emoji', '')
            signature = re.sub(r'1f(\d.+)', '', signature)
            if (len(signature) > 0):
                nlp = SnowNLP(signature)
            emotions.append(nlp.sentiments)
            signatures += ' '.join(jieba.analyse.extract_tags(signature, 5))

            with open('signatures.txt', 'wt', encoding='utf-8') as file:
                file.write(signatures)

    # Sinature WordCloud
    back_coloring = np.array(Image.open('flower.jpg'))
    wordcloud = WordCloud(
        font_path='simfang.ttf',
        background_color="white",
        max_words=1200,
        mask=back_coloring,
        max_font_size=75,
        random_state=45,
        width=960,
        height=720,
        margin=15
    )
    wordcloud.generate(signatures)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    wordcloud.to_file('signatures.jpg')
    # Signature Emotional Judgment
    count_good = len(list(filter(lambda x: x > 0.66, emotions)))
    count_normal = len(list(filter(lambda x: x >= 0.33 and x <= 0.66, emotions)))
    count_bad = len(list(filter(lambda x: x < 0.33, emotions)))
    labels = [u'负面消极', u'中性', u'正面积极']
    values = (count_bad, count_normal, count_good)
    plt.rcParams['font.sans-serif'] = ['simHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel(u'情感判断', fontproperties=font_set)
    plt.ylabel(u'频数', fontproperties=font_set)
    plt.xticks(range(3), labels)
    plt.legend(loc='upper right')
    plt.bar(range(3), values, color='rgb')
    plt.title(u'%s的微信好友签名信息情感分析' % friends[0]['NickName'], fontproperties=font_set)
    plt.show()
