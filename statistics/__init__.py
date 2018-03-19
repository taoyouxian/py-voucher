#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : PRIterator.py.py
@Author: taoyx
@Contact : taoyouxian@ruc.edu.cn 
@Date  : 2018/3/18 14:04
@Desc  : 
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# s = pd.Series([1, 3, 5, np.nan, 6, 8])
# print(s)
# dates = pd.date_range('20130101', periods=6)
# print(dates)
# df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
# print(df)
# print(df.head())
location = pd.io.parsers.read_csv('location.csv')
# print(location.head())
# print(location.tail())
# print(location.ix[[0, 2, 4, 5, 7]])
# print(location.describe())
dic = {'NickName': ['tao'], 'Province': ['安徽'], 'City': ['马鞍山']}
location2 = pd.DataFrame(dic)
location3 = pd.concat([location, location2])
# print(location3)
location4 = location.drop([0, 2, 4, 6])
# print(location4)

