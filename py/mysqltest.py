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
from bs4 import BeautifulSoup
import time
citys=['中国','国际'
    ,'北京','天津','上海','重庆','内蒙古','新疆','宁夏','广西'
    , '西藏', '河北', '山西', '吉林', '辽宁', '黑龙江', '陕西', '甘肃'
    , '青海', '山东', '福建', '浙江', '河南', '湖北', '湖南', '江西'
    , '江苏', '安徽', '广东', '海南', '四川', '贵州', '云南', '台湾']
for city in citys:
    time.sleep(1)
    data = {'objName': city,
            'realCardNumber':''}
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'host':'shixin.csrc.gov.cn',
               'Origin':'http://shixin.csrc.gov.cn',
               'Referer':'http://shixin.csrc.gov.cn/honestypub/'}
    r = requests.post(url='http://shixin.csrc.gov.cn/honestypub/honestyObj/query.do',data =data,headers = headers)
    #print(r.text)
    html=r.text
    # 可选择 Beautiful Soup 解析 http://cuiqingcai.com/1319.html
    soup = BeautifulSoup(html)
    #print(soup.prettify())
    tagas=soup.find_all('a')
    for taga in tagas :
        short_url=taga['href']
        if(short_url!='http://www.csrc.gov.cn'):
           # print(taga['href'])
            url='http://shixin.csrc.gov.cn'+short_url
            res= requests.post(url=url)
            #print(res.text)
            content=BeautifulSoup(res.text)
            tag=content.find('td', text='违法违规失信者姓名')
            name_text=None
            if(tag!=None):
                tag=tag.parent
                name_text=tag.find('td',bgcolor="#FFFFFF").get_text()
                print('违法违规失信者姓名='+name_text)
            if(tag==None):
                tag = content.find('td', text='违法违规失信者名称')
                tag = tag.parent
                name_text = tag.find('td', bgcolor="#FFFFFF").get_text()
                print('违法违规失信者名称=' + name_text)


            tag = content.find('td', text='组织机构代码')
            code_text=None
            if(tag!=None):
                tag = tag.parent
                code_text = tag.find('td', bgcolor="#FFFFFF").get_text()
                print('组织机构代码=' + code_text)

            tag = content.find('td', text='处罚处理时间')
            tag = tag.parent
            date_text = tag.find('td', bgcolor="#FFFFFF").get_text()
            print('处罚处理时间=' + date_text)

            tag = content.find('td', text='处罚处理机构')
            tag = tag.parent
            tag = tag.find('td', bgcolor="#FFFFFF").get_text()
            print('处罚处理机构=' + tag)

            tag = content.find('td', text='处罚处理种类')
            tag = tag.parent
            category_text = tag.find('td', bgcolor="#FFFFFF").get_text()
            print('处罚处理种类=' + category_text)

            tag = content.find('td', text='处罚处理内容')
            tag = tag.parent
            short_detail_url = tag.find('td', bgcolor="#FFFFFF").find('a')['href']
            detail_url='http://shixin.csrc.gov.cn'+short_detail_url
            detail_res= requests.post(detail_url)
            detail_html=detail_res.text
            detail_soup=BeautifulSoup(detail_html)
            detail_body=detail_soup.find('textarea')
            detail_text=detail_body.get_text()
            #print(type(detail_text))
            print('处罚处理内容=' + detail_body.get_text())

            # FIXME 数据入库
            #content_tables= content.find_all('table',cellpadding='5')#,"{'cellpadding':'5','cellspacing':'1','bgcolor':'#CCCCCC'}"
            #for content_table in content_tables:
            #    print(type(content_table['tbody']))
            #table_body=BeautifulSoup(content_table[0])
            #print(table_body)
            print(city+'====================================================================================')
       # t=BeautifulSoup(taga.string)
        #print(t.get_attribute_list('href'))

'''
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print
        '遇到的开始标签：%s' % tag

    def handle_endtag(self, tag):
        print
        '遇到的结束标签：%s' % tag

    def handle_data(self, data):
        print
        '遇到的内容：%s' % data
m=MyHTMLParser()
m.feed('<H3>标题三</H3>')
'''

#需要安装chromedreiver,不同版本对应的也不一样
'''
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
print(title)'''
#browser.quit()


