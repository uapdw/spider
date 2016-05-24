# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import GZCiitNewsLoader


class GZCiitNewsSpider(LoaderMappingSpider):
    '''贛州市人力资源和社会保障局爬虫'''

    name = 'gzciit_gov_cn_news'
    allowed_domains = [
        'gzciit.gov.cn',
    ]
    start_urls = ['http://www.gzciit.gov.cn/']

    mapping = {
        '.*/t\d+_\d+.html': GZCiitNewsLoader
    }