# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cxtc_com.cxtc_com_news import (
    CxtcComNewsLoader
)


class CxtcComNewSpider(LoaderMappingSpider):

    u"""厦门钨业股份有限公司新闻爬虫"""

    name = 'cxtc_com_news'
    allowed_domains = [
        'cxtc.com'
    ]
    start_urls = ['http://www.cxtc.com/']

    mapping = {
        'cxtc\.com/getNews\.html\?l2menu\.uid=\d+&news\.uid=\d+':
        CxtcComNewsLoader
    }
