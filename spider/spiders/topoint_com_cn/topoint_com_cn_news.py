# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import TopointNewsLoader


class TopointNewsSpider(LoaderMappingSpider):

    u"""支点网新闻爬虫"""

    name = 'topoint_com_cn_news'
    allowed_domains = ['www.topoint.com.cn']
    start_urls = ['http://www.topoint.com.cn/']

    mapping = {
        'http://www.topoint.com.cn/html/article/\d{4}/\d+/\d+.html':
        TopointNewsLoader
    }
