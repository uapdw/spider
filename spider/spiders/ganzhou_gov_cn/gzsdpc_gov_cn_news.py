# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import GZSdpcNewsLoader


class GZSdpcNewsSpider(LoaderMappingSpider):
    '''赣州市发展和改革委员会爬虫'''

    name = 'gzsdpc_gov_cn_news'
    allowed_domains = [
        'gzsdpc.gov.cn',
    ]
    start_urls = ['http://www.gzsdpc.gov.cn/']

    mapping = {
        '.*/t\d+_\d+.htm': GZSdpcNewsLoader
    }