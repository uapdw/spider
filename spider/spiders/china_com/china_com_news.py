# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import ChinaNewsLoader


class ChinaNewsSpider(LoaderMappingSpider):
    '''中华网新闻爬虫'''

    name = 'china_com_news'
    allowed_domains = [
        'news.china.com',
        'ent.china.com',
        'economy.china.com',
        'money.china.com',
        'tech.china.com',
    ]
    start_urls = ['http://www.china.com/index.html']

    mapping = {
        '\w+\.china.com/\w+/\w*/\d+/\d{8}/\d{8}_all.html': ChinaNewsLoader
    }
