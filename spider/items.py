# -*- coding: utf-8 -*-

import datetime

from scrapy.item import Item, Field
from scrapy.exceptions import DropItem

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, DateTime, DECIMAL, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://uradar:uradar@172.20.19.132/greatwall?charset=utf8'
SQLALCHEMY_POOL_RECYCLE = 60 * 60 * 2  # 2 hours, same as uradar


engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_recycle=SQLALCHEMY_POOL_RECYCLE,
    encoding='utf-8'
)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class RequiredFieldItem(Item):
    def validate(self):
        for required_field in self.required_fields:
            if required_field not in self or not self[required_field]:
                raise DropItem('not field %s' % required_field)


class SqlalchemyItem(RequiredFieldItem):

    def add(self):
        self.validate()

        ModelClass = self.model
        session = Session()
        try:
            row = ModelClass()
            for key in self['row'].keys():
                setattr(row, self['row'][key])
            session.add(row)
            session.commit()
        except (SqlalchemyIntegrityError, PymysqlIntegrityError) as e:
            session.rollback()
            raise DropItem(e.message)
        except Exception as e:
            session.rollback()
            raise DropItem(e.message)
        finally:
            session.close()


class CurrListedCorp(Base):
    __tablename__ = 'curr_listed_corp'

    stock_cd = Column(String(6), primary_key=True)
    corp_name = Column(String(500))
    indus = Column(String(100))

    stock_sname = Column(String(20))
    corp_sname = Column(String(100))


class CurrListedCorpItem(SqlalchemyItem):
    required_fields = ['stock_cd', 'corp_name', 'indus']
    model = CurrListedCorp

    stock_cd = Field()
    corp_name = Field()
    indus = Field()

    stock_sname = Field()
    corp_sname = Field()


class PeriodList(Base):
    __tablename__ = 'period_list'

    year = Column(String(4), primary_key=True)
    period = Column(String(8), primary_key=True)


class PeriodListItem(SqlalchemyItem):
    required_fields = ['year', 'period']
    model = PeriodList

    year = Field()
    period = Field()


class SpiderProcessInfo(Base):
    __tablename__ = 'spider_process_info'

    corp_stock_cd = Column(String(6), primary_key=True)
    year = Column(String(4))
    period = Column(String(8))
    data_sour = Column(String(1000))


class SpiderProcessInfoItem(SqlalchemyItem):
    required_fields = ['corp_stock_cd', 'year', 'period']
    model = SpiderProcessInfo

    corp_stock_cd = Field()
    year = Field()
    period = Field()
    data_sour = Field()


class ListedCorpInfo(Base):
    __tablename__ = 'listed_corp_info'

    data_sour = Column(String(1000))
    year = Column(String(4))
    period = Column(String(8))
    stock_cd = Column(String(6), primary_key=True)
    stock_sname = Column(String(20))
    corp_sname = Column(String(50))
    corp_name = Column(String(500))
    eh_name = Column(String(100))
    indus = Column(String(50))
    reg_addr = Column(String(1000))
    corp_url = Column(String(200))
    legal_reps = Column(String(10))
    corp_sec = Column(String(10))
    reg_cap = Column(DECIMAL(24, 2))
    post_cd = Column(String(6))
    corp_tel = Column(String(15))
    corp_fax = Column(String(20))
    email = Column(String(50))
    listed_time = Column(Date)
    raise_cap = Column(Date)
    issue_qty = Column(Integer)
    issue_price = Column(DECIMAL(24, 2))
    issue_pe_ratio = Column(DECIMAL(12, 6))
    issue_way = Column(String(20))
    main_underw = Column(String(50))
    listed_referr = Column(String(50))
    recomm_org = Column(String(100))
    is_crawl = Column(String(2))
    modifytime = Column(String(19))


class ListedCorpInfoItem(SqlalchemyItem):
    required_fields = ['stock_cd', 'year', 'period']
    model = ListedCorpInfo

    data_sour = Field()
    year = Field()
    period = Field()
    stock_cd = Field()
    stock_sname = Field()
    corp_sname = Field()
    corp_name = Field()
    eh_name = Field()
    indus = Field()
    reg_addr = Field()
    corp_url = Field()
    legal_reps = Field()
    corp_sec = Field()
    reg_cap = Field()
    post_cd = Field()
    corp_tel = Field()
    corp_fax = Field()
    email = Field()
    listed_time = Field()
    raise_cap = Field()
    issue_qty = Field()
    issue_price = Field()
    issue_pe_ratio = Field()
    issue_way = Field()
    main_underw = Field()
    listed_referr = Field()
    recomm_org = Field()
    is_crawl = Field()
    modifytime = Field()


class StockReport(Base):
    __tablename__ = 'stock_report'

    report_id = Column(String(36), primary_key=True)
    stock_code = Column(String(45))
    publish_time = Column(DateTime)
    report_name = Column(String(255))
    pdf_url = Column(String(255))
    pdf_path = Column(String(255))


class StockReportItem(Item):
    stock_code = Field()
    publish_time = Field()
    report_name = Field()

    file_urls = Field()
    files = Field()


class HBaseItem(Item):

    # hbase 表名
    table_name = None

    # hbase 列族
    column_family = 'column'

    # md5后作为主键的列
    row_key_field = None

    # 必须字段，如果没有值丢弃item
    required_fields = []

    def validate(self):
        for required_field in self.required_fields:
            if required_field not in self or not self[required_field]:
                raise DropItem('not field %s' % required_field)

        publish_time = getattr(self, 'publish_time', None)
        if isinstance(publish_time, datetime.datetime) and \
                publish_time > datetime.datetime.now():
            raise DropItem('invalid publish_time %s' % publish_time)

    def get_row_key(self):
        return self[self.row_key_field]


class UradarWeiboItem(HBaseItem):
    table_name = 'uradar_weibo'

    required_fields = ['weibo_id', 'weibo_url', 'content', 'created_at']

    weibo_id = Field()
    weibo_url = Field()
    content = Field()
    created_at = Field()

    user_url = Field()
    screen_name = Field()
    user_pic = Field()

    comment_count = Field()
    repost_count = Field()

    def get_row_key(self):
        return self['weibo_url']


class UradarBBSItem(HBaseItem):
    table_name = 'uradar_bbs'
    required_fields = ['thread_id', 'post_id', 'url', 'title', 'content',
                       'publish_time']

    thread_id = Field()
    post_id = Field()

    url = Field()
    title = Field()
    abstract = Field()
    keywords = Field()
    content = Field()
    author = Field()
    publish_time = Field()

    source = Field()

    site_domain = Field()
    site_name = Field()

    sentiment = Field()

    def get_row_key(self):
        return '%s_%s_%s' % (self['site_domain'], self['thread_id'],
                             self['post_id'])


class UradarArticleItem(HBaseItem):

    table_name = 'uradar_article'
    row_key_field = 'url'
    required_fields = ['url', 'title', 'content', 'publish_time']

    url = Field()
    title = Field()
    author = Field()
    abstract = Field()
    content = Field()
    publish_time = Field()
    source = Field()  # 文章来源
    keywords = Field()

    article_type = Field()  # 文章类型
    site_domain = Field()
    site_name = Field()

    add_time = Field()
    sentiment = Field()


class UradarNewsItem(UradarArticleItem):

    def __init__(self):
        super(UradarNewsItem, self).__init__(article_type='1')


class UradarBlogItem(UradarArticleItem):

    def __init__(self):
        super(UradarBlogItem, self).__init__(article_type='3')


class UradarWeixinItem(UradarArticleItem):

    def __init__(self):
        super(UradarWeixinItem, self).__init__(article_type='2')


class UradarReportItem(UradarArticleItem):

    def __init__(self):
        super(UradarReportItem, self).__init__(article_type='4')


class UradarActivityItem(HBaseItem):

    table_name = 'uradar_activity'
    row_key_field = 'url'
    required_fields = ['url', 'title', 'start_time', 'end_time']

    url = Field()
    title = Field()
    start_time = Field()
    end_time = Field()
    location = Field()
    trad = Field()
    content = Field()
    keywords = Field()

    source_domain = Field()
    source_name = Field()
    add_time = Field()


class CarComDetailItem(HBaseItem):

    table_name = 'car_com_detail'
    row_key_field = 'comment_id'
    required_fields = ['comment_id', 'product_id', 'url', 'content', 'author', 'publish_time']

    comment_id = Field()
    product_id = Field()
    url = Field()
    author = Field()
    content = Field()
    publish_time = Field()
    sentiment = Field()


class CarDanPinItem(HBaseItem):

    table_name = 'car_danpin'
    row_key_field = 'product_id'
    required_fields = ['product_id', 'brand', 'type']

    product_id = Field()
    brand = Field()
    type = Field()
