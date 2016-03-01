# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import EworksNewsLoader


class EworksNewsSpider(LoaderMappingSpider):

    u"""e-works新闻爬虫"""

    name = 'eworks_net_cn_news'
    allowed_domains = ['e-works.net.cn']
    start_urls = ['http://www.e-works.net.cn/']

    mapping = {
        'http://\w+.e-works.net.cn/\w+/\w+.htm': EworksNewsLoader
    }
