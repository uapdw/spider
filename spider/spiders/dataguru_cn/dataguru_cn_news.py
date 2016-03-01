# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import DataguruNewsLoader


class DataguruNewsSpider(LoaderMappingSpider):

    u"""炼数成金新闻爬虫"""

    name = 'dataguru_cn_news'
    allowed_domains = ['dataguru.cn']
    start_urls = ['http://dataguru.cn/']

    mapping = {
        'dataguru\.cn/article-\d+-\d+\.html': DataguruNewsLoader
    }
