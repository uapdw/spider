# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.minmetals_com_cn.minmetals_com_cn_news import (
    MinmetalsComCnNewsLoader
)


class MinmetalsComCnNewSpider(LoaderMappingSpider):

    u"""中国五矿集团公司新闻爬虫"""

    name = 'minmetals_com_cn_news'
    allowed_domains = ['minmetals.com.cn']
    start_urls = ['http://www.minmetals.com.cn/']

    mapping = {
        'minmetals\.com\.cn/.*?/\d+/t\d+_\d+\.html':
        MinmetalsComCnNewsLoader
    }
