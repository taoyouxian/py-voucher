#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : friend.py.py
@Author: taoyx
@Contact : taoyouxian@ruc.edu.cn 
@Date  : 2018/3/14 18:10
@Desc  : 
'''
import itchat

from wechat.headImage import analyseHeadImage
from wechat.location import analyseLocation
from wechat.sex import analyseSex
from wechat.signature import analyseSignature

itchat.auto_login(hotReload=True)

friends = itchat.get_friends(update=True)

# print(friends)

# analyseSex(friends)
# analyseLocation(friends)
analyseHeadImage(friends)
# analyseSignature(friends)