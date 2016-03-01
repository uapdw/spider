# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import ChinaCloudNewsLoader


class ChinaCloudNewsSpider(LoaderMappingSpider):

    u"""中云网新闻爬虫"""

    name = 'china-cloud_com_news'
    allowed_domains = ['china-cloud.com']
    start_urls = ['http://www.china-cloud.com/']

    mapping = {
        'china-cloud\.com/.*/\d{8}_\d+\.html': ChinaCloudNewsLoader
    }
