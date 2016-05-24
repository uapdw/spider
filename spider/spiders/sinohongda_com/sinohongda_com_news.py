# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.sinohongda_com.sinohongda_com_news import (
    SinohongdaComNewsLoader
)


class SinohongdaComNewSpider(LoaderMappingSpider):

    u"""宏达集团新闻爬虫"""

    name = 'sinohongda_com_news'
    allowed_domains = ['sinohongda.com']
    start_urls = ['http://www.sinohongda.com/main/Navigation/lang/zh']

    mapping = {
        'sinohongda\.com/html/news/show_1_\d+_w1_zh.html':
        SinohongdaComNewsLoader
    }
