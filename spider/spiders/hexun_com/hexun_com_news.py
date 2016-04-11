# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import HexunNewsLoader


class HexunNewsSpider(LoaderMappingSpider):

    u"""和讯新闻爬虫"""

    name = 'hexun_com_news'
    allowed_domains = [
        'news.hexun.com',
        'tech.hexun.com',
    ]
    start_urls = ['http://www.hexun.com/']

    mapping = {
        'hexun\.com/\d{4}-\d{2}-\d{2}/\d+\.html': HexunNewsLoader
    }
