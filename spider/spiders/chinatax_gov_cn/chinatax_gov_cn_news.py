# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.chinatax_gov_cn.chinatax_gov_cn_news import(
    ChinataxGovCnNewsLoader
)


class ChinataxGovCnNewsSpider(LoaderMappingSpider):

    u"""国家税务总局新闻爬虫"""

    name = 'chinatax_gov_cn_news'
    allowed_domains = [
        'chinatax.gov.cn'
    ]
    start_urls = ['http://www.chinatax.gov.cn/index.html']

    mapping = {
        'n\d+/n\d+/n\d+/c\d+/content.html':
        ChinataxGovCnNewsLoader
    }
