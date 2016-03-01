# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import SapNewsLoader


class SapNewsSpider(LoaderMappingSpider):

    u"""SAP新闻爬虫"""

    name = 'sap_com_news'
    allowed_domains = ['global.sap.com']
    start_urls = [
        'http://global.sap.com/china/news-reader/index.epx'
    ]

    mapping = {
        '.*china/news-reader/index\.epx\?.*articleID=\d+.*': SapNewsLoader
    }
