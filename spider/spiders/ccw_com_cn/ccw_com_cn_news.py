# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CcwNewsLoader


class CcwNewsSpider(LoaderMappingSpider):

    u"""计世网新闻爬虫"""

    name = 'ccw_com_cn_news'
    allowed_domains = ['www.ccw.com.cn']
    start_urls = ['http://www.ccw.com.cn/']

    mapping = {
        'http://www.ccw.com.cn/article/view/\d+': CcwNewsLoader
    }
