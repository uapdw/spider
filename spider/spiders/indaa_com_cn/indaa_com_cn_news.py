# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.indaa_com_cn.indaa_com_cn_news import(
    IndaaComCnNewsLoader
)


class IndaaComCnNewsSpider(LoaderMappingSpider):

    u"""英大网新闻爬虫"""

    name = 'indaa_com_cn_news'
    allowed_domains = ['indaa.com.cn']
    start_urls = ['http://www.indaa.com.cn/']

    mapping = {
        '.xwzx/\S+/\d{6}/t\d{8}_\d+.html':
        IndaaComCnNewsLoader
    }
