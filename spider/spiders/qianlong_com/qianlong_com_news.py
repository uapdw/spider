# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import QianLongNewsLoader


class QianLongNewsSpider(LoaderMappingSpider):

    u"""千龙网新闻爬虫"""

    name = 'qianlong_com_news'
    allowed_domains = ['qianlong.com']
    start_urls = ['http://www.qianlong.com/']

    mapping = {
        '\w+\.qianlong.com/\d{4}/\d{4}/\d{6}\.shtml': QianLongNewsLoader
    }
