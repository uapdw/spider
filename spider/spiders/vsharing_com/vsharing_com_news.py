# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import VsharingNewsLoader


class VsharingNewsSpider(LoaderMappingSpider):

    u"""畅享网新闻爬虫"""

    name = 'vsharing_com_news'
    allowed_domains = [
        'portal.vsharing.com',
        'it.vsharing.com',
        'www.vsharing.com',
    ]
    start_urls = ['http://www.vsharing.com/']

    mapping = {
        'http://www.vsharing.com/\w+/\w+/\d{4}-\d+/\d+.html':
        VsharingNewsLoader
    }
