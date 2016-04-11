# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import EastDayNewsLoader


class EastDayNewsSpider(LoaderMappingSpider):
    '''东方网新闻爬虫'''

    name = 'eastday_com_news'
    allowed_domains = [
        'news.eastday.com',
        'sh.eastday.com',
        'finance.eastday.com',
        'shzw.eastday.com',
        'world.eastday.com',
        'china.eastday.com',
    ]
    start_urls = ['http://www.eastday.com/']

    mapping = {
        '\w+\.eastday.com/\w+/\d{8}/\w+.html': EastDayNewsLoader
    }
