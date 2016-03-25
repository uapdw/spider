# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CnsoftNewsLoader


class CnsoftNewsSpider(LoaderMappingSpider):

    u"""中国软件资讯网新闻爬虫"""

    name = 'cnsoftnews_com_news'
    allowed_domains = ['www.cnsoftnews.com']
    start_urls = ['http://www.cnsoftnews.com/']

    mapping = {
        'http://www.cnsoftnews.com/\w+/\d+/\d+.html': CnsoftNewsLoader
    }
