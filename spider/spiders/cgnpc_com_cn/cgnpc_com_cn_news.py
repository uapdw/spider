# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cgnpc_com_cn.cgnpc_com_cn_news import(
    CgnpcComCnNewsLoader
)


class CgnpcComCnNewsSpider(LoaderMappingSpider):

    u"""中广核新闻爬虫"""

    name = 'cgnpc_com_cn_news'
    allowed_domains = ['cgnpc.com.cn']
    start_urls = ['http://www.cgnpc.com.cn/']

    mapping = {
        'n\d+/n\d+/n\d+/c\d+/content.html'or
        'n\d+/n\d+/c\d+/content.html':
        CgnpcComCnNewsLoader
    }
