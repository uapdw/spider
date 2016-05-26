# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.ndrc_gov_cn.ndrc_gov_cn_news import(
        NdrcGovCnNewsLoader
)


class NdrcGovCnNewsSpider(LoaderMappingSpider):

    u"""中华人民共和国国家发展和改革委员会爬虫"""

    name = 'ndrc_gov_cn_news'
    allowed_domains = [
        'ndrc.gov.cn'
    ]
    start_urls = ['http://www.ndrc.gov.cn/']

    mapping = {
        'www.ndrc.gov.cn/xwzx/xwfb/\d{6}/t\d{8}_\d+.html':
        NdrcGovCnNewsLoader
    }
