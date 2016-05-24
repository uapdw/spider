# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.shmet_com.shmet_com_news import (
    ShmetComNewsLoader
)


class ShmetComNewsSpider(LoaderMappingSpider):

    u"""上海金属网新闻爬虫"""

    name = 'shmet_com_news'
    allowed_domains = ['shmet.com']
    start_urls = ['http://www.shmet.com/Home.html']

    mapping = {
        'shmet\.com/cms/c\-\d+\.html': ShmetComNewsLoader
    }
