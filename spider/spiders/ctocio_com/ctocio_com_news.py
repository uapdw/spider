# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CtocioNewsLoader


class CtocioNewsSpider(LoaderMappingSpider):

    u"""IT经理网新闻爬虫"""

    name = 'ctocio_com_news'
    allowed_domains = ['ctocio.com']
    start_urls = ['http://www.ctocio.com/']

    mapping = {
        'ctocio\.com/ccnews/\d+\.html': CtocioNewsLoader
    }
