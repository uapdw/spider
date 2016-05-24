# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cnitdc_com.cnitdc_com_news import (
    CnitdcComNewsLoader
)


class CnitdcComNewsSpider(LoaderMappingSpider):

    u"""中国有色金属科技信息网新闻爬虫"""

    name = 'cnitdc_com_news'
    allowed_domains = ['cnitdc.com']
    start_urls = ['http://www.cnitdc.com/']

    mapping = {
        'cnitdc\.com/htm/\d+/\d+\.htm': CnitdcComNewsLoader
    }
