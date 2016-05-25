# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import GZHrssNewsLoader


class GZHrssNewsSpider(LoaderMappingSpider):
    '''贛州市人力资源和社会保障局爬虫'''

    name = 'gzhrss_gov_cn_news'
    allowed_domains = [
        'gzhrss.gov.cn',
    ]
    start_urls = ['http://www.gzhrss.gov.cn/']

    mapping = {
        '.*/content.html': GZHrssNewsLoader
    }
