import pymysql
import requests
#from bs4 import BeautifulSoup
import ssl
from lxml import etree
import time
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
## 数据库先不用管
conn = pymysql.connect(host='10.77.110.224', port=3306, user='root', passwd='Root_1230',db='wechatspider',charset='utf8')

## 可能需要设置登陆cookie ，先自己写，有问题看下别人如何处理 代理ip的
### 打开搜狗微信链接
timestamp=int(round(time.time() * 1000))
count=0
#http://weixin.sogou.com/weixin

headers = {'content-type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
           'host': 'weixin.sogou.com',
           'Origin': 'http://weixin.sogou.com/weixin',
           'Referer': 'http://weixin.sogou.com/weixin',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept - Encoding': 'gzip, deflate',
           'Cookie':'SUV=0017177ECA7072CB5A33C9FB466C5908; ABTEST=3|1514182161|v1; IPLOC=CN1100; SUID=9DB66ADA2930990A000000005A409611; SUID=46D5786A3108990A000000005A409611; weixinIndexVisited=1; JSESSIONID=aaaezR1RvJ0dwfrRMMw8v; ppinf=5|1514364036|1515573636|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlQUQlOTklRTYlOTklOTMlRTUlODUlODl8Y3J0OjEwOjE1MTQzNjQwMzZ8cmVmbmljazoyNzolRTUlQUQlOTklRTYlOTklOTMlRTUlODUlODl8dXNlcmlkOjQ0Om85dDJsdUhWdnlTYmFMV0FiV29ac1E5N01vc29Ad2VpeGluLnNvaHUuY29tfA; pprdig=YgUcbwU-6Q4FFI6teziDxkEkVnDtjhzvr7Cvyw47_Rsa1nV_ilPCTgjxSWlpJKco4xQwRMz1XAlB_LpLaTqvA0gWFhyifF7uUCayji8hlhryGFhdoI6wdWYaye7936zrVzcX-YFL7pe-d_7_IiIUYMvxJw2ex0vn2ITcSb0M8b8; sgid=19-32696065-AVpDXIQZ8ibI1eYmEcS87QuM; ppmdig=15143640370000003f88ad82c6f780917c785a57cba66ac8; PHPSESSID=6gp1qt8u44pkmhl2ttfd4ktdm2; SUIR=C0EB37875D593D785E3870465D1DF8EF; SNUID=AC1416AD66620729C2E725CC67CC955A; seccodeRight=success; successCount=3|Wed, 27 Dec 2017 09:03:09 GMT; sct=10'}
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
        id=(count-1)*10+index;
        print(id)
        # print(abstract)
        body_req=requests.get(url)
        body_req.encoding='utf-8'
        body_root=etree.HTML(body_req.content)
        body=body_root.xpath('string(//div[@id="js_content"])')
        time.sleep(1)
        # print(body)
    print('----------------'+str(count)+'--------------------------')
### 从第一页开始解析
    time.sleep(1)
### 对于每一页，再解析每页中的具体文章内容，保存文章标题和内容

### 结束 ，进入下一页

