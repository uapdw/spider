# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import YnetNewsLoader


class YnetNewsSpider(LoaderMappingSpider):

    u"""北青网新闻爬虫"""

    name = 'ynet_com_news'
    allowed_domains = ['ynet.com']
    start_urls = ['http://www.ynet.com/']

    mapping = {
        'news\.ynet\.com/[\d\.]+/\d{4}/\d{2}/\d+\.html': YnetNewsLoader
    }
