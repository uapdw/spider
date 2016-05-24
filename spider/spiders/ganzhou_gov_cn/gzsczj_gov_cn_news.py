# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import GZSCZJNewsLoader


class GZSCZJNewsSpider(LoaderMappingSpider):
    '''赣州市财政局爬虫'''

    name = 'gzsczj_gov_cn_news'
    allowed_domains = [
        'gzsczj.gov.cn',
    ]
    start_urls = ['http://www.gzsczj.gov.cn/']

    mapping = {
        '.*/\d{8}.*.html': GZSCZJNewsLoader
    }
