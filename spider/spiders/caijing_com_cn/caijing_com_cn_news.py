# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CaijingNewsLoader


class CaijingNewsSpider(LoaderMappingSpider):

    u"""财经网新闻爬虫"""

    name = 'caijing_com_cn_news'
    allowed_domains = ['caijing.com.cn']
    start_urls = ['http://www.caijing.com.cn/']

    mapping = {
        'caijing\.com\.cn/\d{8}/\d+\.shtml': CaijingNewsLoader
    }
