# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.csg_cn.csg_cn_news import(
    CsgCnNewsLoader
)


class CsgCnNewsSpider(LoaderMappingSpider):

    u"""中国南方电网新闻爬虫"""

    name = 'csg_cn_news'
    allowed_domains = ['csg.cn']
    start_urls = ['http://www.csg.cn/']

    mapping = {
        './\S+/\d{4}/\S+/\d{6}/t\d{8}_\d+.html':
        CsgCnNewsLoader
    }
