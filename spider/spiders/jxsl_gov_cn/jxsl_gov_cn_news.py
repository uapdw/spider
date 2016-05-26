# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.jxsl_gov_cn.jxsl_gov_cn_news import (
    JxslGovCnNewsLoader
)


class JxslGovCnNewsSpider(LoaderMappingSpider):

    u"""江西省水利厅新闻爬虫"""

    name = 'jxsl_gov_cn_news'
    allowed_domains = ['jxsl.gov.cn']
    start_urls = ['http://www.jxsl.gov.cn/']

    mapping = {
        'jxsl\.gov\.cn/.*?/\d{4}/\S+\.html':
        JxslGovCnNewsLoader
    }
