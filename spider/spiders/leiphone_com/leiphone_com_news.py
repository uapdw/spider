# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import LeiphoneNewsLoader


class LeiphoneNewsSpider(LoaderMappingSpider):

    u"""雷锋网新闻爬虫"""

    name = 'leiphone_com_news'
    allowed_domains = [
        'www.leiphone.com',
    ]
    start_urls = ['http://www.leiphone.com/']

    mapping = {
        'leiphone\.com/news/\d{6}/\S+\.html': LeiphoneNewsLoader
    }
