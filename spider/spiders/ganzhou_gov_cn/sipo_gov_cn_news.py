# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import SiPoNewsLoader


class SiPoNewsSpider(LoaderMappingSpider):
    '''全国知识产权局系统政府门户网站-江西子站爬虫'''

    name = 'sipo_gov_cn_news'
    allowed_domains = [
        'sipo.gov.cn',
    ]
    start_urls = ['http://www.sipo.gov.cn/']

    mapping = {
        '.*/t\d+_\d+.htm': SiPoNewsLoader
    }