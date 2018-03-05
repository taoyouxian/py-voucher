import requests
from lxml import etree
import time
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import random
import re


def filter_emoji(desstr, restr=''):
    '''
    过滤表情和html标签
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


def filter_html(desstr, restr=''):
    '''
    过滤表情和html标签
    '''
    try:
        co = re.compile(r'<[^>]+>', re.S)  # 过滤html标签
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'host': 's.weibo.com',
    'Origin': 'https://m.weibo.cn/',
    'Referer': 'https://m.weibo.cn/p/100103type%3D1%26q%3D%E4%BD%9B%E7%B3%BB?type=all&queryVal=%E4%BD%9B%E7%B3%BB&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title=%E4%BD%9B%E7%B3%BB',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Cookie': 'SINAGLOBAL=6343442846856.146.1513347568320; _s_tentry=-; Apache=3518059681162.209.1514387933166; ULV=1514387933171:9:9:2:3518059681162.209.1514387933166:1514178427038; SWBSSL=usrmdinst_11; SWB=usrmdinst_7; login_sid_t=f8c8cb152bac7f485b1534d750077eae; cross_origin_proto=SSL; UOR=,,login.sina.com.cn; SCF=AsA9hxzgTDLUhcTMV3LTO5K0UmnQMfNkzil-wPpyg9PEkCXBPMtqRB9094kRIZhU7Mcl-2jbIqR5r8CGHulYJkU.; SUB=_2A253R5PlDeThGedL4lAV-S3IzDyIHXVUNIItrDV8PUNbmtANLRDRkW9NVELpaB0Zgazb5atVcKupmTLSrXFhgS-N; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF6hbeyo6KV8aRbhwQ5MFsl5JpX5KzhUgL.Fo2f1KzX1KeXS052dJLoI79jqg4XUgzt; SUHB=0qjliQP767f2G0; ALF=1545934645; SSOLoginState=1514398645; wvr=6; WBStorage=c1cc464166ad44dc|undefined',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    'X-API-Version': '3.0.91',
    'X-App-Za': 'OS=Web',
    'X-UDID': 'ABCCwujc5QyPTmGj5bKNc_pE9mSxfJrI0-4='
}
month = input('请输入月，默认10月 \n')
if (month == ''):
    month = 10
dayStart = input('请输入日，默认1日\n')
if (dayStart == ''):
    dayStart = 1
month = int(month)
dayStart = int(dayStart)
while dayStart < 30:
    dayEnd = dayStart + 1
    pageNum = 1;
    while pageNum <= 50:
        hasMore = True
        url = 'http://s.weibo.com/weibo/%25E4%25BD%259B%25E7%25B3%25BB&typeall=1&suball=1&timescope=custom:2017-' + str(
            month) + '-' + str(
            dayStart) + '-0:2017-' + str(month) + '-' + str(dayEnd) + '-0&page=' + str(pageNum)
        req = requests.get(url=url, headers=headers)
        root = etree.HTML(req.content)
        lines = root.xpath('//script[starts-with(text(),"STK && STK.pageletM && STK.pageletM.view(")]')
        index = 0
        isCaught = True
        for line in lines:
            text = line.text
            if (text.startswith('STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct"')):
                isCaught = False
                n = text.find('html":"')
                substr = text[n + 7: -12]
                print(substr)
                j = substr.encode("utf8", 'ignore').decode('unicode_escape', 'ignore').encode("utf8", 'ignore').decode(
                    "utf8", 'ignore').replace(
                    '\\', '')
                # print(j)
                if (j.find('<div class="search_noresult">') > 0):
                    hasMore = False
                    print('sssssss')
                    ## 有结果的页面
                else:
                    # 此处j要decode，因为上面j被encode成utf-8了
                    page = etree.HTML(j)
                    ps = page.xpath('//p[@node-type="feed_list_content"]')  # 使用xpath解析得到微博内容
                    addrs = page.xpath('//a[@class="W_texta W_fb"]')  # 使用xpath解析得到博主地址
                    addri = 0
                    # 获取昵称和微博内容
                    for p in ps:
                        name = filter_html(filter_emoji(p.attrib.get('nick-name'))).replace(' ', '')  # 获取昵称
                        txt = filter_html(filter_emoji(p.xpath('string(.)'))).replace(' ', '')  # 获取微博内容
                        if (dayStart < 10):
                            id = int(str(month) + '0' + str(dayStart)) * 1000 + (pageNum - 1) * 20 + index
                        else:
                            id = int(str(month) + str(dayStart)) * 1000 + (pageNum - 1) * 20 + index
                        print(str(id) + ':' + name + ':' + txt)
                        Base = declarative_base()


                        class PublishDetail(Base):
                            # 表名称
                            __tablename__ = 'weibo_html'
                            # 表结构
                            id = Column(Integer, primary_key=True)
                            title = Column(String(255))
                            content = Column(String)


                        # 初始化数据库连接:  使用pymysql 官方文档为: http://docs.sqlalchemy.org/en/latest/dialects/index.html
                        engine = create_engine('mysql+pymysql://tao:tao@10.77.40.27:3306/py_voucher?charset=utf8',
                                               encoding='utf8', convert_unicode=True)
                        # 创建DBSession类型:
                        DBSession = sessionmaker(bind=engine)
                        session = DBSession()
                        weibo_html = PublishDetail(id=id, title=name, content=txt)
                        session.add(weibo_html)
                        session.commit()
                        session.close()

                        index += 1
        printstr = str(month) + '.' + str(dayStart) + '.' + str(pageNum)
        if (isCaught):
            print('is Caught! 时间为:' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            status = input('请输入 quit 退出，继续请随意输入 \n')
            if (status == 'quit'):
                print('结束id规则为:' + printstr)
                exit()
        if (not hasMore):
            print(printstr + ' 无数据')
            break
        print(printstr + ' 完成...')
        sleep_time_one = random.randint(10, 15)
        sleep_time_two = random.randint(15, 20)
        if (pageNum % 2 == 0):
            time.sleep(sleep_time_two)
        else:
            time.sleep(sleep_time_one)
        pageNum += 1
    dayStart += 1
