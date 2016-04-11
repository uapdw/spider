# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CiotimesNewsLoader


class CiotimesNewsSpider(LoaderMappingSpider):

    u"""CIO时代新闻爬虫"""

    name = 'ciotimes_com_news'
    allowed_domains = ['www.ciotimes.com']
    start_urls = ['http://www.ciotimes.com/']

    mapping = {
        'ciotimes\.com/\S+/\d+\.html': CiotimesNewsLoader
    }
