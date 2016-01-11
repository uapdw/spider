# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader


"""添加所有爬虫到爬虫管理系统
现在source_type都是news，不是的需要改过来
source_site用allowed_domains第一个，但是爬虫管理系统校验时把它当目录来用
所以要和目录名一致才行
"""


Base = declarative_base()


class Spider(Base):
    __tablename__ = 'spider_info'

    spider_id = Column(String(24), primary_key=True)
    name = Column(String)
    tag = Column(String)
    source_type = Column(String)
    source_url = Column(String)
    source_site = Column(String)
    code_path = Column(String)
    note = Column(String)
    creator = Column(String)
    creation_time = Column(DateTime)
    modifier = Column(String)
    modify_time = Column(DateTime)
    project = Column(String)
    result_store_desc = Column(String)
    enable = Column(String)
    schedule_config = Column(String)
    alert_receiver = Column(String)
    status = Column(String)


some_engine = create_engine(
    'mysql+pymysql://root:udh*123@172.20.8.115/uspider_manager?charset=utf8mb4'
)
Session = sessionmaker(bind=some_engine)


def add_spiders():

    settings = get_project_settings()
    spider_loader = SpiderLoader(settings)

    spiders = [
        spider_loader.load(spider_name) for spider_name in spider_loader.list()
    ]

    session = Session()

    stored_spiders = session.query(Spider).all()
    stored_spider_names = set([spider.name for spider in stored_spiders])
    stored_spider_ids = set([spider.spider_id for spider in stored_spiders])

    skip_list = []

    for spider in spiders:
        name = getattr(spider, 'name', None)
        start_urls = getattr(spider, 'start_urls', None)
        allowed_domains = getattr(spider, 'allowed_domains', None)

        if name in stored_spider_names:
            skip_list.append(name)
            continue
        if not start_urls or not allowed_domains or len(start_urls) != 1 \
                or len(allowed_domains) != 1:
            print 'name: %s' % name
            print 'start_urls: %s' % start_urls
            print 'allowed_domains: %s' % allowed_domains
            print
            continue

        spider = Spider()
        spider.spider_id = hex(random.getrandbits(96))[2:-1]
        while True:
            if spider.spider_id in stored_spider_ids:
                spider.spider_id = hex(random.getrandbits(96))[2:-1]
            else:
                break
        spider.name = name
        spider.tag = ''
        spider.source_type = 'news'
        spider.source_url = start_urls[0]
        spider.source_site = allowed_domains[0]
        spider.code_path = name
        spider.note = ''
        spider.creator = '2nvr3z0th110cffgaztk'
        spider.creation_time = datetime.datetime.now()
        spider.modifier = '2nvr3z0th110cffgaztk'
        spider.modify_time = datetime.datetime.now()
        spider.project = u'默认'
        spider.result_store_desc = ''
        spider.enable = 1
        spider.schedule_config = 'once_a_day'
        spider.alert_receiver = ''
        spider.status = 'init'
        session.add(spider)

    session.commit()

    print 'skipped spiders: '
    for spider in skip_list:
        print spider


add_spiders()
