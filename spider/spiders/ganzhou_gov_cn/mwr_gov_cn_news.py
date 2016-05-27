# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import MWRNewsLoader


class MWRNewsSpider(LoaderMappingSpider):
    '''国家水利部爬虫'''

    name = 'mwr_gov_cn_news' 
    allowed_domains = [ 'mwr.gov.cn', ]
    start_urls = ['http://www.mwr.gov.cn/']

    mapping = {
        '.*/t\d+_\d+.html': MWRNewsLoader
    }