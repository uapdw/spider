# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cut35_com.cut35_com_news import (
    Cut35ComNewsLoader
)


class Cut35ComNewsSpider(LoaderMappingSpider):

    u"""中国刀具商务网新闻爬虫"""

    name = 'cut35_com_news'
    allowed_domains = [
        'cut35.com'
    ]
    start_urls = ['http://www.cut35.com/']

    mapping = {
        'cut35\.com/info/\d+\.html':
        Cut35ComNewsLoader
    }
