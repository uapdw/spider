# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import N199itNewsLoader


class N199itNewsSpider(LoaderMappingSpider):

    u"""199it新闻爬虫"""

    name = '199it_com_news'
    allowed_domains = ['www.199it.com']
    start_urls = ['http://www.199it.com/']

    mapping = {
        '199it\.com/archives/\d+\.html': N199itNewsLoader
    }
