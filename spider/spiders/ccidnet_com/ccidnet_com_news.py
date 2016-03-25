# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CcidnetNewsLoader


class CcidnetNewsSpider(LoaderMappingSpider):

    u"""赛迪网新闻爬虫"""

    name = 'ccidnet_com_news'
    allowed_domains = ['www.ccidnet.com']
    start_urls = ['http://www.ccidnet.com/']

    mapping = {
        'ccidnet\.com/\d{4}/\d{4}/\d+\.shtml': CcidnetNewsLoader
    }
