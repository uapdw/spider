# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import GmwNewsLoader


class GmwNewsSpider(LoaderMappingSpider):

    u"""光明网新闻爬虫"""

    name = 'gmw_cn_news'
    allowed_domains = ['gmw.cn']
    start_urls = ['http://gmw.cn/']

    mapping = {
        'gmw\.cn/\d{4}-\d{2}/\d{2}/content_\d+\.htm': GmwNewsLoader
    }
