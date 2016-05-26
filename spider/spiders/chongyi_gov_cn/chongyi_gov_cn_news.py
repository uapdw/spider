# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.chongyi_gov_cn.chongyi_gov_cn_news import (
    ChongyiGovCnNewsLoader
)


class ChongyiGovCnSpider(LoaderMappingSpider):

    u"""崇义县人民政府新闻爬虫"""

    name = 'chongyi_gov_cn_news'
    allowed_domains = [
        'chongyi.gov.cn'
    ]
    start_urls = [
        'http://www.chongyi.gov.cn/'
    ]

    mapping = {
        'chongyi\.gov\.cn/.*?/\d{6}/t\d+_\d+\.html': ChongyiGovCnNewsLoader
    }
