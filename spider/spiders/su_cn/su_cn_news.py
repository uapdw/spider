# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.su_cn.su_cn_news import(
    SuCnNewsLoader
)


class SuCnNewsSpider(LoaderMappingSpider):

    u"""石油网新闻爬虫"""

    name = 'su_cn_news'
    allowed_domains = ['s-u.cn']
    start_urls = ['http://www.s-u.cn/']

    mapping = {
        'news.s-u.cn/\d{8}/\d+.html':
        SuCnNewsLoader
    }
