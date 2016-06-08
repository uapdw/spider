# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cpnn_com_cn.cpnn_com_cn_news import(
    CpnnComCnNewsLoader
)


class CpnnComCnNewsSpider(LoaderMappingSpider):

    u"""中国电力新闻网新闻爬虫"""

    name = 'cpnn_com_cn_news'
    allowed_domains = ['cpnn.com.cn']
    start_urls = ['http://www.cpnn.com.cn/']

    mapping = {
        './\S+/\d{6}/t\d{8}_\d+.html':
        CpnnComCnNewsLoader
    }
