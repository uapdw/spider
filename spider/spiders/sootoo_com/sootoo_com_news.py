# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import SootooNewsLoader


class SootooNewsSpider(LoaderMappingSpider):

    u"""速途网新闻爬虫"""

    name = 'sootoo_com_news'
    allowed_domains = [
        'www.sootoo.com',
        'it.sootoo.com',
    ]
    start_urls = ['http://www.sootoo.com/']

    mapping = {
        'http://www.sootoo.com/content/\d+.shtml': SootooNewsLoader
    }
