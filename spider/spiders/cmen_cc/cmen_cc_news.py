# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cmen_cc.cmen_cc_news import(
    CmenCcNewsLoader
)


class CmenCcNewsSpider(LoaderMappingSpider):

    u"""国家能源网新闻爬虫"""

    name = 'cmen_cc_news'
    allowed_domains = ['cmen.cc']
    start_urls = ['http://www.cmen.cc/']

    mapping = {
        'www.cmen.cc/\S+/\d{4}_\d{2}_\d{2}_\d+.shtml':
        CmenCcNewsLoader
    }
