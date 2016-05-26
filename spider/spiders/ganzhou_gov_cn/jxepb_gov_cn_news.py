# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import JXEpbNewsLoader


class JXEpbNewsSpider(LoaderMappingSpider):
    '''江西省环境保护厅爬虫'''

    name = 'jxepb_gov_cn_news' 
    allowed_domains = [ 'jxepb.gov.cn', ]
    start_urls = ['http://www.jxepb.gov.cn/']

    mapping = {
        '.*/\d{4}/.*.htm': JXEpbNewsLoader
    }