# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.oil_inen_com.oil_inen_com_news import(
    OilInenComNewsLoader
)


class OilInenComNewsSpider(LoaderMappingSpider):

    u"""国际石油网新闻爬虫"""

    name = 'oil_inen_com_news'
    allowed_domains = ['oil.in-en.com']
    start_urls = ['http://oil.in-en.com/']

    mapping = {
        'oil.in-en.com/html/oil-\d+.shtml':
        OilInenComNewsLoader
    }
