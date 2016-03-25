# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CbismbNewsLoader


class CbismbNewsSpider(LoaderMappingSpider):

    u"""中小企业IT网新闻爬虫"""

    name = 'cbismb_com_news'
    allowed_domains = ['www.cbismb.com']
    start_urls = ['http://www.cbismb.com/']

    mapping = {
        'cbismb\.com/.*/news/\d{4}-\d{2}-\d{2}/\d+\.html': CbismbNewsLoader
    }
