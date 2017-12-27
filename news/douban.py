import pymysql
import requests
#from bs4 impolrt BeautifulSoup
import ssl
from lxml import etree
import time
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import re
def filter_emoji(desstr,restr=''):
    '''
    过滤表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)

timestamp=int(round(time.time() * 1000))
count=input('请输入其实页码 \n')
if(count==''):
    count=0
else:
    count=int(count)-1
print(count)
headers = {
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
           'host': 'www.douban.com',
           'Origin': 'https://www.zhihu.com/',
           'Referer': 'https://www.douban.com/group/search?start=50&cat=1013&sort=relevance&q=%E4%BD%9B%E7%B3%BB',
           'Accept': 'application/json, text/plain, */*',
           'Accept-Encoding': 'gzip, deflate',
           'Cookie':'bid=39dKRdkpA_g; ll="108288"; ps=y; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1514379437%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DlimMKkNCEW00W5CBGJvCMjXNHiDrLgGtw6HzA76XQCG%26wd%3D%26eqid%3D808ca49300069ae5000000025a4398a9%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.763252804.1513522682.1514252740.1514379438.5; __utmc=30149280; __utmz=30149280.1514379438.5.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; _pk_id.100001.8cb4=577e40bc2f4dd51f.1513522663.6.1514379720.1514252744.; __utmb=30149280.71.9.1514379719763',
           'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
           'X-API-Version':'3.0.91',
           'X-App-Za':'OS=Web',
           'X-UDID':'ABCCwujc5QyPTmGj5bKNc_pE9mSxfJrI0-4='
            }
while(count<1000):
    data = {'cat': 1013,
            'sort': 'relevance',  # 不变
            'q': '佛系',  # 内容
            'start': count}  # 开始数----
    req = requests.get(url='https://www.douban.com/group/search', params=data, headers=headers)
    req.encoding='utf-8'
    html=req.text
    #print (html)
    root = etree.HTML(req.content)
    ### 获取总共多少页，从第一页开始解析 写死 总共780页
    # print(html)

    items=root.xpath('//tbody/tr[@class="pl"]')
    #print(len(items))
    index=0
    for item in items:
        index+=1
        id=count+index
        title=item.xpath('string(./td[@class="td-subject"])')
        print(title)
        url=item.xpath('./td[@class="td-subject"]/a/@href')[0]
        body_req=requests.get(url)
        body_req.encoding='utf-8'
        body_root=etree.HTML(body_req.content)
        content=body_root.xpath('string(//div[@class="topic-content"])')
        lis=body_root.xpath('//ul[@id="comments"]/li')
        if(len(lis)>0):
            for li in lis:
                content+=li.xpath('string(./div[@class="reply-doc content"]/p)')
        print(content)
        Base = declarative_base()
        class PublishDetail(Base):
            # 表名称
            __tablename__ = 'douban'
            # 表结构
            id = Column(Integer, primary_key=True)
            title = Column(String(255))
            abstract = Column(String(511))
            content = Column(String)


        # 初始化数据库连接:  使用pymysql 官方文档为: http://docs.sqlalchemy.org/en/latest/dialects/index.html
        engine = create_engine('mysql+pymysql://root:Root_1230@10.77.110.224:3306/news?charset=utf8',
                               encoding='utf8', convert_unicode=True)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        douban = PublishDetail(id=id, title=filter_emoji(title), abstract=filter_emoji(title),
                              content=filter_emoji(content).replace(' ', ''))
        session.add(douban)
        session.commit()
        session.close()
        print('---------------------id='+str(id)+'------------------------')
        time.sleep(1.5)
    count+=50
