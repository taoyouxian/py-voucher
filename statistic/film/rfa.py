#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : rfa.py.py
@Author: taoyx
@Contact : taoyouxian@ruc.edu.cn 
@Date  : 2018/3/21 10:04
@Desc  : 
'''

from urllib import request

from PIL import Image
from bs4 import BeautifulSoup as bs
import re
import jieba
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import matplotlib
from os import path

matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud

def genClound(words_stat):
    d = path.dirname(__file__)
    alice_mask = numpy.array(Image.open(path.join(d, "flower.png")))
    # 用词云进行显示
    wordcloud = WordCloud(font_path="simhei.ttf", background_color="white", mask=alice_mask, max_font_size=120)
    word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}
    # word_frequence_list = []
    # for key in word_frequence:
    #     temp = (key, word_frequence[key])
    #     word_frequence_list.append(temp)
    # print(word_frequence_list)
    # print(dict(word_frequence_list))
    # print(dict(word_frequence_list).items())
    wordcloud = wordcloud.fit_words(word_frequence)
    wordcloud.to_file('output.png')
    # show
    plt.imshow(wordcloud)
    plt.axis("off")
    # plt.figure()
    # plt.imshow(alice_mask, cmap=plt.cm.gray)
    # plt.axis("off")
    plt.show()

def clearData(eachCommentList):
    # 将列表中的数据转换为字符串
    comments = ''
    for k in range(len(eachCommentList)):
        comments = comments + (str(eachCommentList[k])).strip()
    print(comments)
    # 使用正则表达式去除标点符号
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comments)
    cleaned_comments = ''.join(filterdata)
    # print(cleaned_comments)
    # 使用结巴分词进行中文分词
    segment = jieba.lcut(cleaned_comments)
    words_df = pd.DataFrame({'segment': segment})
    print(len(words_df))
    # print(words_df.describe())
    # 去掉停用词
    stopwords = pd.read_csv("stopwords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'],
                            encoding='utf-8')  # quoting=3全不引用
    # print(stopwords)
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
    # print(len(words_df))
    # 统计词频
    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
    # words_stat = words_df.groupby('segment')['segment'].agg({"计数": numpy.size}).sort_values(by=["计数"], ascending=False)
    # print(words_stat)
    # print(words_stat.index)
    genClound(words_stat)

def getComment(param):
    # requrl = 'https://movie.douban.com/subject/' + nowplaying_list[0]['id'] + '/comments' + '?' + 'start=0' + '&limit=20'
    # 爬取评论函数
    requrl = 'https://movie.douban.com/subject/' + param + '/comments' + '?' + 'start=0' + '&limit=20'
    resp = request.urlopen(requrl)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    comment_div_lits = soup.find_all('div', class_='comment')

    eachCommentList = []
    # i = 0
    for item in comment_div_lits:
        if item.find_all('p')[0].string is not None:
            eachCommentList.append(item.find_all('p')[0].string)
            # print(str(i) + ", " + item.find_all('p')[0].string)
        # else:
        #     print(i)
        # i += 1
    # print(len(eachCommentList))
    clearData(eachCommentList)

def getFilmInfo(filmName):
    # 分析网页函数
    resp = request.urlopen('https://movie.douban.com/nowplaying/beijing/')
    html_data = resp.read().decode('utf-8')
    # print(html_data)
    soup = bs(html_data, 'html.parser')
    nowplaying_movie = soup.find_all('div', id='nowplaying')
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
    nowplaying_list = []
    flag = False
    for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']
        for tag_img_item in item.find_all('img'):
            nowplaying_dict['name'] = tag_img_item['alt']
            nowplaying_list.append(nowplaying_dict)
            if (nowplaying_dict['name'] == filmName):
                getComment(nowplaying_dict['id'])
                flag = True
                break
        if (flag is True):
            break
    # print(nowplaying_list)


getFilmInfo('红海行动')

