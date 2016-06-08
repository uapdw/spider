# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.inengyuan_com.inengyuan_com_news import(
    InengyuanComNewsLoader
)


class InengyuanComNewsSpider(LoaderMappingSpider):

    u"""能源经济网新闻爬虫"""

    name = 'inengyuan_com_news'
    allowed_domains = ['inengyuan.com']
    start_urls = ['http://www.inengyuan.com/']

    mapping = {
        'www.inengyuan.com/\d{4}/\S+_\d{4}/\d+.html':
        InengyuanComNewsLoader
    }
