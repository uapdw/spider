# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import QudongNewsLoader


class QudongNewsSpider(LoaderMappingSpider):

    u"""驱动中国新闻爬虫"""

    name = 'qudong_com_news'
    allowed_domains = [
        'news.qudong.com',
    ]
    start_urls = ['http://www.qudong.com/']

    mapping = {
        'qudong\.com/\d{4}/\d{4}/\d+\.shtml': QudongNewsLoader
    }
