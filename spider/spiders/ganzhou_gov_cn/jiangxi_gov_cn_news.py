# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import JiangXiNewsLoader


class JiangXiNewsSpider(LoaderMappingSpider):
    '''江西省人民政府爬虫'''

    name = 'jiangxi_gov_cn_news'
    allowed_domains = [
        'jiangxi.gov.cn',
    ]
    start_urls = ['http://jiangxi.gov.cn/']

    mapping = {
        '.*/\d{6}/t\d+_\d+.html': JiangXiNewsLoader
    }