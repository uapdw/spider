# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import ChinaComCnNewsLoader


class ChinaComCnNewsSpider(LoaderMappingSpider):

    u"""中国网新闻爬虫"""

    name = 'china_com_cn_news'
    allowed_domains = [
        'news.china.com.cn',
        'finance.china.com.cn',
        'business.china.com.cn',
        'tech.china.com.cn',
        'invest.china.com.cn',
    ]
    start_urls = ['http://www.china.com.cn/']

    mapping = {
        'china\.com\.cn/\d{4}-\d{2}/\d{2}/content_\d+\.htm':
        ChinaComCnNewsLoader,
        'china\.com\.cn/.*/\d{8}/\d+\.shtml': ChinaComCnNewsLoader
    }
