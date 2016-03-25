# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import YCWBNewsLoader


class YCWBNewsSpider(LoaderMappingSpider):
    '''金羊网新闻爬虫'''

    name = 'ycwb_com_news'
    allowed_domains = [
        'news.ycwb.com',
        'sp.ycwb.com',
        'money.ycwb.com',
        '3c.ycwb.com',
    ]
    start_urls = ['http://www.ycwb.com/']

    mapping = {
        '\w+\.ycwb.com/\d{4}-\d{2}/\d+/\w+.htm': YCWBNewsLoader
    }
