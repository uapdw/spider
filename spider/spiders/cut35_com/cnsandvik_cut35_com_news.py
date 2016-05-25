# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cut35_com.cut35_com_news import (
    CnsandvikCut35ComNewsLoader
)


class Cut35ComNewsSpider(LoaderMappingSpider):

    u"""中国刀具商务网新闻爬虫"""

    name = 'cnsandvik_cut35_com_news'
    allowed_domains = [
        'cnsandvik.cut35.com'
    ]
    start_urls = [
        'http://cnsandvik.cut35.com/'
    ]

    mapping = {
        'cnsandvik\.cut35\.com/info/\S+\.html':
        CnsandvikCut35ComNewsLoader
    }
