# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import N36dsjNewsLoader


class N36dsjNewsSpider(LoaderMappingSpider):

    u"""36dsj新闻爬虫"""

    name = '36dsj_com_news'
    allowed_domains = ['www.36dsj.com']
    start_urls = ['http://www.36dsj.com/']

    mapping = {
        '36dsj\.com/archives/\d+': N36dsjNewsLoader
    }
