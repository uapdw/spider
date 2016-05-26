# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.jxcc_com.jxcc_com_news import (
    JxccComNewsLoader
)


class JxccComNewSpider(LoaderMappingSpider):

    u"""江铜集团新闻爬虫"""

    name = 'jxcc_com_news'
    allowed_domains = [
        'jxcc.com'
    ]
    start_urls = ['http://www.jxcc.com/index.html']

    mapping = {
        'jxcc\.com/.*?/\d{8}/jt_\d+\.html': JxccComNewsLoader
    }
