# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import GZ315NewsLoader


class GZ315NewsSpider(LoaderMappingSpider):
    '''赣州市工商行政管理局爬虫'''

    name = 'gz315_gov_cn_news'
    allowed_domains = [
        'gz315.gov.cn',
    ]
    start_urls = ['http://www.gz315.gov.cn/']

    mapping = {
        'ganzhou/.*/\d+/\d+.html': GZ315NewsLoader
    }