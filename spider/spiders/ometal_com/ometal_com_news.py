# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.ometal_com.ometal_com_news import (
    OmetalComNewsLoader
)


class OmetalComNewsSpider(LoaderMappingSpider):

    u"""全球金属网新闻爬虫"""

    name = 'ometal_com_news'
    allowed_domains = [
        'ometal.com'
    ]
    start_urls = [
        'http://www.ometal.com/news_other.htm'
    ]

    mapping = {
        'ometal\.com/bin/new/\d{4}/\d+/\d+/other/\d+\.htm': OmetalComNewsLoader
    }
