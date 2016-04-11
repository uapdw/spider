# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import N100ecNewsLoader


class N100ecNewsSpider(LoaderMappingSpider):

    u"""中国电子商务研究中心新闻爬虫"""

    name = '100ec_cn_news'
    allowed_domains = ['www.100ec.cn']
    start_urls = ['http://www.100ec.cn']

    mapping = {
        '100ec\.cn/detail--\d+\.html': N100ecNewsLoader
    }
