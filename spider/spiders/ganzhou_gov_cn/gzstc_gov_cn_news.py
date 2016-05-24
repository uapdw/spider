# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import GZStcNewsLoader


class GZStcNewsSpider(LoaderMappingSpider):
    '''赣州市科技局爬虫'''

    name = 'gzstc_gov_cn_news'
    allowed_domains = [
        'gzstc.gov.cn',
    ]
    start_urls = ['http://www.gzstc.gov.cn/']

    mapping = {
        'article-\d+-\d+.aspx': GZStcNewsLoader
    }
