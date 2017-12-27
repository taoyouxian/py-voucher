import pymysql
import requests
#from bs4 impolrt BeautifulSoup
import ssl
from lxml import etree
import time
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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
## 数据库先不用管
conn = pymysql.connect(host='10.77.110.224', port=3306, user='root', passwd='Root_1230',db='news',charset='utf8')

## 可能需要设置登陆cookie ，先自己写，有问题看下别人如何处理 代理ip的
### 打开搜狗微信链接
timestamp=int(round(time.time() * 1000))
count=input('请输入其实页码 \n')
if(count==''):
    count=0
else:
    count=int(count)-1
print(count)
#http://weixin.sogou.com/weixin

headers = {'content-type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
           'host': 'weixin.sogou.com',
           'Origin': 'http://weixin.sogou.com/weixin',
           'Referer': 'http://weixin.sogou.com/weixin',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept - Encoding': 'gzip, deflate',
           'Cookie':'SUV=0017177ECA7072CB5A33C9FB466C5908; ABTEST=3|1514182161|v1; IPLOC=CN1100; SUID=9DB66ADA2930990A000000005A409611; SUID=46D5786A3108990A000000005A409611; weixinIndexVisited=1; JSESSIONID=aaaezR1RvJ0dwfrRMMw8v; ppinf=5|1514364036|1515573636|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlQUQlOTklRTYlOTklOTMlRTUlODUlODl8Y3J0OjEwOjE1MTQzNjQwMzZ8cmVmbmljazoyNzolRTUlQUQlOTklRTYlOTklOTMlRTUlODUlODl8dXNlcmlkOjQ0Om85dDJsdUhWdnlTYmFMV0FiV29ac1E5N01vc29Ad2VpeGluLnNvaHUuY29tfA; pprdig=YgUcbwU-6Q4FFI6teziDxkEkVnDtjhzvr7Cvyw47_Rsa1nV_ilPCTgjxSWlpJKco4xQwRMz1XAlB_LpLaTqvA0gWFhyifF7uUCayji8hlhryGFhdoI6wdWYaye7936zrVzcX-YFL7pe-d_7_IiIUYMvxJw2ex0vn2ITcSb0M8b8; sgid=19-32696065-AVpDXIQZ8ibI1eYmEcS87QuM; PHPSESSID=6gp1qt8u44pkmhl2ttfd4ktdm2; SUIR=C0EB37875D593D785E3870465D1DF8EF; sct=15; ppmdig=1514367293000000ab4970b0e0afd6430cbfd881485004b5; seccodeErrorCount=1|Wed, 27 Dec 2017 10:22:58 GMT; SNUID=64DDC07AAFB5CEE018B6CD0FB0263474; seccodeRight=success; successCount=1|Wed, 27 Dec 2017 10:23:05 GMT'}
while(count<780):
    count=count+1;
    data = {'type': 2,
            's_from': 'input',  # 不变
            'query': '佛系',  # 内容
            'ie': 'utf8',  # 不变
            '_sug_': 'n',
            '_sug_type_': '',
            # 'w':'',
            # 'sut':'',
            # 'sst0':timestamp,#时间戳
            # 'lkt':'',
            'page': count}  # 页码----
    req = requests.get(url='http://weixin.sogou.com/weixin', params=data, headers=headers)
    #req = requests.get(url='http://weixin.sogou.com/weixin', data=data, headers=headers)

    req.encoding='utf-8'
    html=req.text
    #print (html)
    root = etree.HTML(req.content)
    ### 获取总共多少页，从第一页开始解析 写死 总共780页
    print(html)

    items=root.xpath('//ul[@class="news-list"]/li/div[@class="txt-box"]')
    while(len(items)<1):
        print('反爬虫开启，请手动验证验证吗，重新从'+str(count)+'页开始')
        exit()
    #print(items)
    index=0
    for item in items:
        index+=1
        #print(item)
        url=item.xpath('./h3/a/@href')[0]
        title= item.xpath('string(./h3/a)')
        abstract=item.xpath('string(./p)')
        #print(url)
        print(title)
        main_id=(count-1)*10+index;
        print(main_id)
        # print(abstract)
        body_req=requests.get(url)
        body_req.encoding='utf-8'
        body_root=etree.HTML(body_req.content)
        body=body_root.xpath('string(//div[@id="js_content"])')

        Base = declarative_base()
        class PublishDetail(Base):
            # 表名称
            __tablename__ = 'weixin'
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
        weixin = PublishDetail(id=main_id, title=filter_emoji(title), abstract=filter_emoji(abstract), content=filter_emoji(body).replace(' ',''))
        try:
            session.add(weixin)
        except IOError:
            print('a')
        else:
            session.commit()
        session.close()
        time.sleep(1)
        print(body)
    print('----------------'+str(count)+'--------------------------')
### 从第一页开始解析
    time.sleep(1)
### 对于每一页，再解析每页中的具体文章内容，保存文章标题和内容

### 结束 ，进入下一页

