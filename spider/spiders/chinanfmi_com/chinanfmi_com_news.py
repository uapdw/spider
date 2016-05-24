# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.chinanfmi_com.chinanfmi_com_news import (
    ChinanfmiComNewsLoader
)


class ChinanfmiComNewsSpider(LoaderMappingSpider):

    u"""中国矿冶设备供求网新闻爬虫"""

    name = 'chinanfmi_com_news'
    allowed_domains = ['chinanfmi.com']
    start_urls = ['http://www.chinanfmi.com/']

    mapping = {
        'chinanfmi\.com/news/show\.php\?itemid=\d+': ChinanfmiComNewsLoader
    }
