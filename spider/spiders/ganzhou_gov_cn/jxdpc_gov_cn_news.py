# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import JXDpcNewsLoader


class JXDpcNewsSpider(LoaderMappingSpider):
    '''江西省发改委爬虫'''

    name = 'jxdpc_gov_cn_news' 
    allowed_domains = [ 'jxdpc.gov.cn', ]
    start_urls = ['http://www.jxdpc.gov.cn/']

    mapping = {
        '.*/\d{6}/t\d+_\d+.htm': JXDpcNewsLoader
    }