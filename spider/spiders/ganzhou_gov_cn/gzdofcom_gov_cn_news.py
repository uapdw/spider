# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import GZDoFComNewsLoader


class GZDoFComNewsSpider(LoaderMappingSpider):
    '''赣州市商务局爬虫'''

    name = 'gzdofcom_gov_cn_news'
    allowed_domains = [
        'gzdofcom.gov.cn',
    ]
    start_urls = ['http://www.gzdofcom.gov.cn/']

    mapping = {
        '.*/content.html': GZDoFComNewsLoader
    }
