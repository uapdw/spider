# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.saic_gov_cn.saic_gov_cn_news import(
    SaicGovCnNewsLoader
)

class SaicGovCnNewsSpider(LoaderMappingSpider):

    u"""中华人民共和国国家工商行政管理总局新闻爬虫"""

    name = 'saic_gov_cn_news'
    allowed_domains = ['saic.gov.cn']
    start_urls = ['http://www.saic.gov.cn/']

    mapping = {
        './ywdt/\S+/\S+/xxb/\d{6}/t\d{8}_\d+.html':
        SaicGovCnNewsLoader
    }
