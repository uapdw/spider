# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.nengbank_com.nengbank_com_news import(
    NengbankComNewsLoader
)


class NengbankComNewsSpider(LoaderMappingSpider):

    u"""能源创客聚乐部新闻爬虫"""

    name = 'nengbank_com_news'
    allowed_domains = ['nengbank.com']
    start_urls = ['http://www.nengbank.com/']

    mapping = {
        'www.nengbank.com/\S+/\d+.html':
        NengbankComNewsLoader
    }
