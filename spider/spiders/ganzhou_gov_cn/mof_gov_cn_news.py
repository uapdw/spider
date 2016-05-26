# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import MOFNewsLoader


class MOFNewsSpider(LoaderMappingSpider):
    '''国家财政部爬虫'''

    name = 'mof_gov_cn_news'
    allowed_domains = [
        'mof.gov.cn',
    ]
    start_urls = ['http://www.mof.gov.cn/index.htm']

    mapping = {
        '.*/t\d+_\d+.html?': MOFNewsLoader
    }