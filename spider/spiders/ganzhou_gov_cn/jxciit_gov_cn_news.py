# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import JXCiitNewsLoader


class JXCiitNewsSpider(LoaderMappingSpider):
    '''江西省工信部爬虫'''

    name = 'jxciit_gov_cn_news' 
    allowed_domains = [ 'jxciit.gov.cn', ]
    start_urls = ['http://www.jxciit.gov.cn/']

    mapping = {
        'Item/\d+.aspx': JXCiitNewsLoader
    }