import pymysql
# 苍天s上
'''conn = pymysql.connect(host='114.115.137.143', port=3306, user='hw_sxg', passwd='123456',db='py_voucher')
#  数据库编码是否不正确，连接生产实例查询不到数据，怎么回事
cur = conn.cursor()

cur.execute("SELECT *  FROM s_base_paper limit 100")

for r in cur.fetchall():

           print(r)

cur.close()

conn.close()'''
'''import sqlalchemy
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine('mysql://hw_sxg:123456@114.115.137.143:3306/py_voucher')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()'''

import  requests
from html.parser import HTMLParser

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

data = {'objName': '北京',
        'realCardNumber':''}
headers = {'content-type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'host':'shixin.csrc.gov.cn',
           'Origin':'http://shixin.csrc.gov.cn',
           'Referer':'http://shixin.csrc.gov.cn/honestypub/'}
r = requests.post(url='http://shixin.csrc.gov.cn/honestypub/honestyObj/query.do',data =data,headers = headers)
print(r.text)
html=r.text


#需要安装chromedreiver,不同版本对应的也不一样

browser = webdriver.Chrome()
browser.get('http://shixin.csrc.gov.cn/honestypub/')
objName=browser.find_element_by_id('objName')
objName.send_keys('河北')
browser.find_element_by_id('querybtn').click()
#tagas=browser.find_element_by_tag_name('a')
tagas=browser.find_elements_by_tag_name('a')
for taga in tagas:
    print(taga.get_attribute('href'))
    taga.click()
print(tagas)
title=browser.title
print(title)
#browser.quit()


