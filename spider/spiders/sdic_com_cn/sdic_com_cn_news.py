# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.sdic_com_cn.sdic_com_cn_news import(
    SdicComCnNewsLoader
)


class SdicComCnNewsSpider(LoaderMappingSpider):

    u"""国家开发投资公司新闻爬虫"""

    name = 'sdic_com_cn_news'
    allowed_domains = ['sdic.com.cn']
    start_urls = ['http://www.sdic.com.cn/cn/index.htm']

    mapping = {
        '/cn/\S+/\S+/\d{4}/\d{2}/\d{2}/\d+.htm':
        SdicComCnNewsLoader
    }
