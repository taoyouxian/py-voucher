import pymysql
import requests
#from bs4 impolrt BeautifulSoup
import ssl
from lxml import etree
import time

from pymysql import MySQLError
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import re
def filter_emoji(desstr,restr=''):
    '''
    过滤表情和html标签
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
        # co = re.compile(r'<[^>]+>', re.S)#过滤html标签
        # desstr=desstr.replace('💕','')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)
def filter_html(desstr,restr=''):
    '''
    过滤表情和html标签
    '''
    try:
        co = re.compile(r'<[^>]+>', re.S)#过滤html标签
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)
headers = {
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
           'host': 'm.weibo.cn',
           'Origin': 'https://m.weibo.cn/',
           'Referer': 'https://m.weibo.cn/p/100103type%3D1%26q%3D%E4%BD%9B%E7%B3%BB?type=all&queryVal=%E4%BD%9B%E7%B3%BB&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title=%E4%BD%9B%E7%B3%BB',
           'Accept': 'application/json, text/plain, */*',
           'Accept-Encoding': 'gzip, deflate',
           'Cookie':'_T_WM=8f2c8cf99e9df55e93cb7fde1c21bb26; ALF=1516990645; SCF=AsA9hxzgTDLUhcTMV3LTO5K0UmnQMfNkzil-wPpyg9PEVlyYVOXf6ynoO4OyR-Ds9Uj-7VXh20xSu5AKljoZxI4.; SUB=_2A253R5PtDeThGedL4lAV-S3IzDyIHXVUyz2lrDV6PUJbktBeLVr_kW1NVELpaAQsITK-Wt7wbp5_1n5_fLmw2CoY; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF6hbeyo6KV8aRbhwQ5MFsl5JpX5K-hUgL.Fo2f1KzX1KeXS052dJLoI79jqg4XUgzt; SUHB=0h1Yy4nRiyM9oA; SSOLoginState=1514398654; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=featurecode%3D20000320%26oid%3D4189735398158197%26luicode%3D10000011%26lfid%3D106003type%253D1%26fid%3D100103type%253D2%2526q%253D%25E4%25BD%259B%25E7%25B3%25BB%26uicode%3D10000011',
           'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
           'X-API-Version':'3.0.91',
           'X-App-Za':'OS=Web',
           'X-UDID':'ABCCwujc5QyPTmGj5bKNc_pE9mSxfJrI0-4='
            }
count=input('请输入其实页码 \n')
if(count==''):
    count=2
else:
    count=int(count)
print(count)
while(count<10000):
    data = {
        'type': 'all',
        't': 'general',  # 不变
        'queryVal': '佛系',  # 内容
        'featurecode': '200000000',  # 不变
        'luicode': '10000011',
        'starttime':'1000000',
        'lfid': '106003type=1',
        'title': '佛系',
        'containerid': '100103type=1&q=佛系',
        'page': count
    }  # 页码----
    req = requests.get(url='https://m.weibo.cn/api/container/getIndex', params=data, headers=headers)
    print(req.text)
    body = json.loads(req.text)
    items = body['data']['cards'][0]['card_group']
    index = 1
    for item in items:
        # print(item)
        id = 10 * (count - 1) + index
        mblog = item['mblog']
        name = mblog['user']['screen_name']
        gender = mblog['user']['gender']
        source = mblog['source']
        content = mblog['text']
        print(id)
        print(name)
        print(gender)
        print(source)
        print(filter_emoji(content))
        Base = declarative_base()


        class PublishDetail(Base):
            # 表名称
            __tablename__ = 'weibo'
            # 表结构
            id = Column(Integer, primary_key=True)
            name = Column(String(255))
            gender = Column(String(511))
            source = Column(String(511))
            content = Column(String)


        # 初始化数据库连接:  使用pymysql 官方文档为: http://docs.sqlalchemy.org/en/latest/dialects/index.html
        engine = create_engine('mysql+pymysql://root:Root_1230@10.77.110.224:3306/news?charset=utf8',
                               encoding='utf8', convert_unicode=True)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        zhihu = PublishDetail(id=id, name=filter_emoji(name), gender=filter_emoji(gender),
                              content=filter_html(filter_emoji(content)).replace(' ', ''),
                              source=filter_emoji(source))
        try:
            session.add(zhihu)
        except pymysql.err.InternalError:
            print('a')
        session.commit()
        session.close()
        print('--------------' + str(id) + '---------------------')
        index += 1
    time.sleep(3)
    count += 1
    # print(req.text)
