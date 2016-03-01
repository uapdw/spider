# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CniiComCnNewsLoader


class CniiComCnNewsSpider(LoaderMappingSpider):

    u"""中国信息产业网新闻爬虫"""

    name = 'cnii_com_cn_news'
    allowed_domains = ['cnii.com.cn']
    start_urls = ['http://www.cnii.com.cn/']

    mapping = {
        'http://www.cnii.com.cn/\w+/\d{4}-\d{2}/\d+/\w+.htm':
        CniiComCnNewsLoader
    }
