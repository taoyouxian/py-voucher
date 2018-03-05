import json
import re
import requests
# from bs4 impolrt BeautifulSoup
import time

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def filter_emoji(desstr, restr=''):
    '''
    过滤表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'host': 'www.zhihu.com',
    'Origin': 'https://www.zhihu.com/',
    'Referer': 'https://www.zhihu.com/search?q=%E4%BD%9B%E7%B3%BB&type=content',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Cookie': 'q_c1=e91f00522e884eb493ae923094c128c2|1513326020000|1513326020000; _zap=196a2f06-b190-4a09-80fe-ea9096114a97; __utma=51854390.643012537.1514181700.1514181700.1514181700.1; __utmz=51854390.1514181700.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.000--|3=entry_date=20171225=1; d_c0="ABCCwujc5QyPTmGj5bKNc_pE9mSxfJrI0-4=|1514364270"; _xsrf=050fb6d5-d896-4cdf-ab50-517d07014966; aliyungf_tc=AQAAAGEOFUwdYQcAy3JwyjVDRn+tl4mk; l_cap_id="YmEzNDE5MGZjNzY5NGVhN2E0NDdhYmI0YmNmYmMzODU=|1514374711|048494608272a87844cc135a96dda929a402bb97"; r_cap_id="YWVkYjdjMTViZjFhNGU0Nzk4ODQ3ODkwZjA5YTExZmY=|1514374711|14af9a4cca4ae4aaf7129a4977d7b2a73997252d"; cap_id="OTI3NzY0MGI2ZTVmNDZmNDk4ZTYwMTQ0NWNiZDE5NDQ=|1514374711|2a4ccb3928b530ccc6e9bb18ebefa68fa4ec456e',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    'X-API-Version': '3.0.91',
    'X-App-Za': 'OS=Web',
    'X-UDID': 'ABCCwujc5QyPTmGj5bKNc_pE9mSxfJrI0-4='
}
timestamp = int(round(time.time() * 1000))
count = input('请输入起始页码 \n')
if (count == ''):
    count = 0
else:
    count = int(count) - 1
print(count)
while 1 > 0:
    data = {
        't': 'general',  # 不变
        'q': '佛系',  # 内容
        'correction': '1',  # 不变
        'search_hash_id': 'fa66b09b277f4369d1eb4f29ac351d7c',
        'offset': count,
        'limit': 20
    }  # 页码----
    req = requests.get(url='https://www.zhihu.com/api/v4/search_v3', params=data, headers=headers)
    body = json.loads(req.text)
    data = body['data']
    if (len(data) > 0):
        index = 0
        for body in data:
            index += 1
            id = index + count
            obj = body['object']
            highlight = body['highlight']
            title = highlight['title'].replace('<em>', '').replace('</em>', '')
            print(obj)
            content = obj['content'].replace('<em>', '').replace('</em>', '')
            desc = obj['excerpt'].replace('<em>', '').replace('</em>', '')
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
            engine = create_engine('mysql+pymysql://tao:tao@10.77.40.27:3306/py_voucher?charset=utf8',
                                   encoding='utf8', convert_unicode=True)
            # 创建DBSession类型:
            DBSession = sessionmaker(bind=engine)
            session = DBSession()
            zhihu = PublishDetail(id=id, title=filter_emoji(title), abstract=filter_emoji(desc),
                                  content=filter_emoji(content).replace(' ', ''))
            session.add(zhihu)
            session.commit()
            session.close()
            print('--------------' + str(id) + '---------------------')
        time.sleep(10)
        count += 20
    else:
        exit()
