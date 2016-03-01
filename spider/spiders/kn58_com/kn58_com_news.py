# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import Kn58NewsLoader


class Kn58NewsSpider(LoaderMappingSpider):

    u"""微客网新闻爬虫"""

    name = 'kn58_com_news'
    allowed_domains = ['kn58.com']
    start_urls = ['http://www.kn58.com/']

    mapping = {
        'kn58\.com/.*/detail_\d{4}_\d{4}/\d+\.html': Kn58NewsLoader
    }
