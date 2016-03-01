# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import ChinabyteNewsLoader


class ChinabyteNewsSpider(LoaderMappingSpider):

    u"""搜狐新闻爬虫"""

    name = 'chinabyte_com_news'
    allowed_domains = ['chinabyte.com']
    start_urls = ['http://chinabyte.com/']

    mapping = {
        'chinabyte\.com/\d+/\d+\.shtml': ChinabyteNewsLoader
    }
