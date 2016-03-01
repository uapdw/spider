# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import ZdnetNewsLoader


class ZdnetNewsSpider(LoaderMappingSpider):

    u"""至顶网新闻爬虫"""

    name = 'zdnet_com_cn_news'
    allowed_domains = ['zdnet.com.cn']
    start_urls = ['http://www.zdnet.com.cn']

    mapping = {
        'zdnet\.com\.cn/.*/\d{4}/\d{4}/\d+\.shtml': ZdnetNewsLoader
    }
