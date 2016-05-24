# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import GanZhouNewsLoader


class GanZhouNewsSpider(LoaderMappingSpider):
    '''贛州人民政府爬虫'''

    name = 'ganzhou_gov_cn_news'
    allowed_domains = [
        'ganzhou.gov.cn',
    ]
    start_urls = ['http://www.ganzhou.gov.cn/']

    mapping = {
        'zwgk/.*/\d{6}/\w\d+_\d+.htm': GanZhouNewsLoader
    }
