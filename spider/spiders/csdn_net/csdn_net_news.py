# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CSDNNewsLoader


class CSDNNewsSpider(LoaderMappingSpider):

    u"""CSDN新闻爬虫"""

    name = 'csdn_net_news'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net']

    mapping = {
        'article/\d{4}-\d{2}-\d{2}/\d+': CSDNNewsLoader
    }
