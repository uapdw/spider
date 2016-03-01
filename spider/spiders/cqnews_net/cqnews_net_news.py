# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CqNewsNetNewsLoader


class CqNewsNetNewsSpider(LoaderMappingSpider):

    u"""华龙网新闻爬虫"""

    name = 'cqnews_net_news'
    allowed_domains = ['cqnews.net']
    start_urls = ['http://www.cqnews.net/']

    mapping = {
        'cq\.cqnews\.net/\S+/\d{4}-\d{2}/\d{2}/content_\d+.htm':
        CqNewsNetNewsLoader
    }
