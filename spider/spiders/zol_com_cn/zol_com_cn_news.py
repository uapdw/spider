# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import ZolNewsLoader


class ZolNewsSpider(LoaderMappingSpider):

    u"""中关村在线新闻爬虫"""

    name = 'zol_com_cn_news'
    allowed_domains = ['zol.com.cn']
    start_urls = ['http://www.zol.com.cn/']

    mapping = {
        'zol\.com\.cn/\d+/\d+\.html': ZolNewsLoader
    }
