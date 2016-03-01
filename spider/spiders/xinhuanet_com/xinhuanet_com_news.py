# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import XinhuanetNewsLoader


class XinhuanetNewsSpider(LoaderMappingSpider):

    u"""新华网新闻爬虫"""

    name = 'xinhuanet_com_news'
    allowed_domains = ['xinhuanet.com']
    start_urls = ['http://xinhuanet.com/']

    mapping = {
        'news\.xinhuanet\.com/\S+/\d{4}-\d{2}/\d{2}/c_\d+.htm':
        XinhuanetNewsLoader
    }
