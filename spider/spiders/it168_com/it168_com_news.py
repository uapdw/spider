# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import It168NewsLoader


class It168NewsSpider(LoaderMappingSpider):

    u"""It168新闻爬虫"""

    name = 'it168_com_news'
    allowed_domains = [
        'cio.it168.com',
        'cloud.it168.com',
        'tech.it168.com',
        'inp.it168.com',
        'datacenter.it168.com',
    ]
    start_urls = ['http://www.it168.com/']

    mapping = {
        'it168\.com/a\d{4}/\d{4}/\d+/\d+\.shtml': It168NewsLoader
    }
