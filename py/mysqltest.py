import pymysql
import sqlalchemy
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class PublishDetail(Base):
    #表名称
    __tablename__='t_publish_detail'
    #表结构
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(127))
    code=Column(String(127))
    date=Column()
    branch=Column(String(127))
    category=Column(String(127))
    content=Column(String)

# 初始化数据库连接:  使用pymysql 官方文档为: http://docs.sqlalchemy.org/en/latest/dialects/index.html
engine = create_engine('mysql+pymysql://hw_sxg:123456@114.115.137.143:3306/py_voucher')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
publish_detail=PublishDetail(name="kkk",code="777",date="2017/05/30",branch="sdffsd",category="kkkk",content="sksksks")
session.add(publish_detail)
session.commit()
session.close()
