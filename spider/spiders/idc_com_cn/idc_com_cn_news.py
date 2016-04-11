# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import IdcNewsLoader


class IdcNewsSpider(LoaderMappingSpider):

    u"""idc新闻爬虫"""

    name = 'idc_com_cn_news'
    allowed_domains = ['www.idc.com.cn']
    start_urls = ['http://www.idc.com.cn/']

    mapping = {
        'idc\.com\.cn/about/press\.jsp\?id=\S+': IdcNewsLoader
    }
