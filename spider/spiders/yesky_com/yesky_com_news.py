# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import YeskyComNewsLoader


class YeskyComNewsSpider(LoaderMappingSpider):

    u"""天极网新闻爬虫"""

    name = 'yesky_com_news'
    allowed_domains = [
        'news.yesky.com',
        'enterprise.yesky.com',
        'cloud.yesky.com',
        'soft.yesky.com',
    ]
    start_urls = ['http://www.yesky.com/']

    mapping = {
        'yesky.com/\d+/\d+.shtml': YeskyComNewsLoader
    }
