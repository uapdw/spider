# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import SohuNewsLoader


class SohuNewsSpider(LoaderMappingSpider):

    u"""搜狐新闻爬虫"""

    name = 'sohu_com_news'
    allowed_domains = ['sohu.com']
    start_urls = ['http://www.sohu.com/']

    mapping = {
        '.*?sohu.com/\d{8}/n\d+.shtml': SohuNewsLoader
    }
