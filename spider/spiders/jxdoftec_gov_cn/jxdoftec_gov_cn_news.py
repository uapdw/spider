# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.jxdoftec_gov_cn.jxdoftec_gov_cn_news import (
    JxdoftecGovCnNewsLoader
)


class JxdoftecGovCnNewsSpider(LoaderMappingSpider):

    u"""江西省商务厅新闻爬虫"""

    name = 'jxdoftec_gov_cn_news'
    allowed_domains = [
        'jxdoftec.gov.cn'
    ]
    start_urls = [
        'http://www.jxdoftec.gov.cn/'
    ]

    mapping = {
        'jxdoftec\.gov\.cn/.*?/\d{6}/t\d{8}_\d+\.htm':
        JxdoftecGovCnNewsLoader
    }
