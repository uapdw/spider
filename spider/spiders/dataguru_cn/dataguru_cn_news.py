# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import DataguruNewsLoader


class DataguruNewsSpider(LoaderMappingSpider):

    u"""炼数成金新闻爬虫"""

    name = 'dataguru_cn_news'
    allowed_domains = [
        'www.dataguru.cn',
        'it.dataguru.cn',
        'bi.dataguru.cn',
        'quant.dataguru.cn',
    ]
    start_urls = ['http://www.dataguru.cn/']

    mapping = {
        'dataguru\.cn/article-\d+-\d+\.html': DataguruNewsLoader
    }
