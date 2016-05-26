# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.gov_cn.gov_cn_news import(
        GovCnNewsLoader
)


class GovCnNewsSpider(LoaderMappingSpider):

    u"""中华人民共和国中央人民政府爬虫"""

    name = 'gov_cn_news'
    allowed_domains = [
        'gov.cn',
    ]
    start_urls = ['http://www.gov.cn/']

    mapping = {
        'www.gov.cn/xinwen/\d{4}-\d{2}/\d{2}/content_\d+.htm':
        GovCnNewsLoader
    }


