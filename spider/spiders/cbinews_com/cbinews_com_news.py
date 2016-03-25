# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CbinewsNewsLoader


class CbinewsNewsSpider(LoaderMappingSpider):

    u"""电脑商情网新闻爬虫"""

    name = 'cbinews_com_news'
    allowed_domains = ['www.cbinews.com']
    start_urls = ['http://www.cbinews.com']

    mapping = {
        'cbinews\.com/\S+/news/\d{4}-\d{2}-\d{2}/\d+\.htm': CbinewsNewsLoader
    }
