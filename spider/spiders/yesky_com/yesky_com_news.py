# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import YeskyComNewsLoader


class YeskyComNewsSpider(LoaderMappingSpider):

    u"""天极网新闻爬虫"""

    name = 'yesky_com_news'
    allowed_domains = ['yesky.com']
    start_urls = ['http://www.yesky.com/']

    mapping = {
        'yesky.com/\d+/\d+.shtml': YeskyComNewsLoader
    }
