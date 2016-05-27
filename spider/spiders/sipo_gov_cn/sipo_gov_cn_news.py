# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.sipo_gov_cn.sipo_gov_cn_news import (
    SipoGovCnNewsLoader
)


class SipoGovCnNewsSpider(LoaderMappingSpider):

    u"""国家知识产权局新闻爬虫"""

    name = 'sipo_gov_cn_news'
    allowed_domains = ['sipo.gov.cn']
    start_urls = ['http://www.sipo.gov.cn/']

    mapping = {
        'sipo\.gov\.cn/.*?/\d{4}/\d{6}/t\d{8}_\d+\.html':
        SipoGovCnNewsLoader
    }
