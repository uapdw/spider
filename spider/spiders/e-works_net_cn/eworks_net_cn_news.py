# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import EworksNewsLoader


class EworksNewsSpider(LoaderMappingSpider):

    u"""e-works新闻爬虫"""

    name = 'eworks_net_cn_news'
    allowed_domains = [
        'news.e-works.net.cn',
        'articles.e-works.net.cn',
        'erp.e-works.net.cn',
        'mes.e-works.net.cn',
        'bpm.e-works.net.cn',
        'scm.e-works.net.cn',
        'eb.e-works.net.cn',
        'cloud2.e-works.net.cn',
        'bigdata.e-works.net.cn',
        'iot.e-works.net.cn',
        'mobileapp.e-works.net.cn',
        'safety.e-works.net.cn',
    ]
    start_urls = ['http://www.e-works.net.cn/']

    mapping = {
        'http://\w+.e-works.net.cn/\w+/\w+.htm': EworksNewsLoader
    }
