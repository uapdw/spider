# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import QQNewsLoader


class QQNewsSpider(LoaderMappingSpider):

    u"""腾讯新闻爬虫"""

    name = 'qq_com_news'
    allowed_domains = ['qq.com']
    start_urls = ['http://qq.com']

    mapping = {
        'news.qq.com/a/\d{8}/\d+.htm': QQNewsLoader
    }
