#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : sex.py
@Author: taoyx
@Contact : taoyouxian@ruc.edu.cn 
@Date  : 2018/3/14 18:24
@Desc  : 
'''
from collections import Counter

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)

def analyseSex(friends):
    sexs = list(map(lambda x: x['Sex'], friends[1:]))
    counts = list(map(lambda x: x[1], Counter(sexs).items()))
    labels = ['Unknow', 'Male', 'Female']
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
    plt.title(u'% s的微信好友性别组成' % friends[0]['NickName'], fontproperties=font_set)
    plt.show()
