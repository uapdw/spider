# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import ChinabyteNewsLoader


class ChinabyteNewsSpider(LoaderMappingSpider):

    u"""搜狐新闻爬虫"""

    name = 'chinabyte_com_news'
    allowed_domains = [
        'news.chinabyte.com',
        'it.chinabyte.com',
        'net.chinabyte.com',
        'e.chinabyte.com',
        'soft.chinabyte.com',
        'bigdata.chinabyte.com',
        'cloud.chinabyte.com',
        'info.chinabyte.com',
        'smb.chinabyte.com',
        'solution.chinabyte.com',
        'do.chinabyte.com',
        'cio.chinabyte.com',
    ]
    start_urls = ['http://chinabyte.com/']

    mapping = {
        'chinabyte\.com/\d+/\d+\.shtml': ChinabyteNewsLoader
    }
