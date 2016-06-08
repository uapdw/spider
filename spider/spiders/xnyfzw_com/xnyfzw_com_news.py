# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.xnyfzw_com.xnyfzw_com_news import(
    XnyfzwComNewsLoader
)


class XnyfzwComNewsSpider(LoaderMappingSpider):

    u"""新能源发展网新闻爬虫"""

    name = 'xnyfzw_com_news'
    allowed_domains = ['xnyfzw.com']
    start_urls = ['http://www.xnyfzw.com/']

    mapping = {
        'www.xnyfzw.com/news/\d{6}/\d{2}/\d+.html':
        XnyfzwComNewsLoader
    }
