# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import MEPNewsLoader


class MEPNewsSpider(LoaderMappingSpider):
    '''国家环境保护部爬虫'''

    name = 'mep_gov_cn_news' 
    allowed_domains = [ 'mep.gov.cn', ]
    start_urls = ['http://www.mep.gov.cn/']

    mapping = {
        '.*/t\d+_\d+.htm': MEPNewsLoader
    }