# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import JXSLNewsLoader


class JXSLNewsSpider(LoaderMappingSpider):
    '''江西省水利厅爬虫'''

    name = 'jxsl_gov_cn_news' 
    allowed_domains = [ 'jxsl.gov.cn', ]
    start_urls = ['http://www.jxsl.gov.cn/']

    mapping = {
        '.*/\d{4}/.*.html': JXSLNewsLoader
    }