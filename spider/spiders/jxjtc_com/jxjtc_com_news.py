# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.jxjtc_com.jxjtc_com_news import (
    JxjtcComNewsLoader
)


class JxjtcComNewSpider(LoaderMappingSpider):

    u"""江西江钨硬质合金有限公司新闻爬虫"""

    name = 'jxjtc_com_news'
    allowed_domains = [
        'jxjtc.com'
    ]
    start_urls = ['http://www.jxjtc.com/index.asp']

    mapping = {
        'jxjtc\.com/article_show\.asp\?id=\d+':
        JxjtcComNewsLoader
    }
