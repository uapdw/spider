# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.jxaic_gov_cn.jxaic_gov_cn_news import (
    JxaicGovCnNewsLoader
)


class JxaicGovCnNewsSpider(LoaderMappingSpider):

    u"""江西省工商行政管理局新闻爬虫"""

    name = 'jxaic_gov_cn_news'
    allowed_domains = ['jxaic.gov.cn']
    start_urls = ['http://www.jxaic.gov.cn/jx/dxzsy.html']

    mapping = {
        'jxaic\.gov\.cn/jx/.*?/\d{8}/\d+\.html':
        JxaicGovCnNewsLoader
    }
