# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CctimeNewsLoader


class CctimeNewsSpider(LoaderMappingSpider):

    u"""飞象网新闻爬虫"""

    name = 'cctime_com_news'
    allowed_domains = ['cctime.com']
    start_urls = ['http://www.cctime.com/']

    mapping = {
        'cctime\.com/html/\d{4}-\d{1,2}-\d{1,2}/\d+\.htm': CctimeNewsLoader
    }
