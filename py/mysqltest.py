import gevent as gevent
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class PublishDetail(Base):
    # 表名称
    __tablename__ = 't_publish_detail'
    # 表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(127))
    code = Column(String(127))
    date = Column()
    branch = Column(String(127))
    category = Column(String(127))
    content = Column(String)


# 初始化数据库连接:  使用pymysql 官方文档为: http://docs.sqlalchemy.org/en/latest/dialects/index.html
engine = create_engine('mysql+pymysql://tao:tao@10.77.40.27:3306/py_voucher')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
publish_detail = PublishDetail(name="kkk", code="777", date="2017/05/30", branch="sdffsd", category="kkkk",
                               content="sksksks")
try:
    session.add(publish_detail)
    session.commit()

    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    detail = session.query(PublishDetail).filter(PublishDetail.id == '739').one()
    # 打印类型和对象的name属性:
    print('type:', type(detail))
    print('name:', detail.name)
    session.close()
except gevent.Timeout:
    session.invalidate()
    raise
except:
    session.rollback()
    raise
