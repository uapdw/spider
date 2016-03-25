# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import PcpopNewsLoader


class PcpopNewsSpider(LoaderMappingSpider):

    u"""泡泡网新闻爬虫"""

    name = 'pcpop_com_news'
    allowed_domains = [
        'news.pcpop.com',
        'smb.pcpop.com',
    ]
    start_urls = ['http://www.pcpop.com/']

    mapping = {
        'pcpop\.com/doc/\d+/\d+/\d+\.shtml': PcpopNewsLoader
    }
