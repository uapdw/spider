# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.dqsy_net.dqsy_net_news import(
    DqsyNetNewsLoader
)


class DqsyNetNewsSpider(LoaderMappingSpider):

    u"""大庆师范学院新闻爬虫"""

    name = 'dqsy_net_news'
    allowed_domains = ['dqsy.net']
    start_urls = ['http://www.dqsy.net/']

    mapping = {
        'info/\d+/\d+.htm':
        DqsyNetNewsLoader
    }
