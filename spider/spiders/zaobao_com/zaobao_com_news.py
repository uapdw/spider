# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.zaobao_com.zaobao_com_news import (
    ZaobaoComNewsLoader
)


class ZaobaoComNewSpider(LoaderMappingSpider):

    u"""联合早报网新闻爬虫"""

    name = 'zaobao_com_news'
    allowed_domains = ['zaobao.com']
    start_urls = ['http://www.zaobao.com/finance']

    mapping = {
        'story\d+-\d+': ZaobaoComNewsLoader
    }
