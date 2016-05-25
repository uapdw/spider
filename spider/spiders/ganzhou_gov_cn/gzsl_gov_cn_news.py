# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import GZSLNewsLoader


class GZSLNewsSpider(LoaderMappingSpider):
    '''赣州市水利局爬虫'''

    name = 'gzsl_gov_cn_news'
    allowed_domains = [
        'gzsl.gov.cn',
    ]
    start_urls = ['http://www.gzsl.gov.cn/']

    mapping = {
        '.*/content.html': GZSLNewsLoader
    }
