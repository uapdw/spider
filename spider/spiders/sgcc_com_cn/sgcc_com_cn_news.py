# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.sgcc_com_cn.sgcc_com_cn_news import(
    SgccComCnNewsLoader
)


class SgccComCnNewsSpider(LoaderMappingSpider):

    u"""国家电网新闻爬虫"""

    name = 'sgcc_com_cn_news'
    allowed_domains = ['sgcc.com.cn']
    start_urls = ['http://www.sgcc.com.cn/index.shtml']

    mapping = {
        '/\S+/\S+/\d+.shtml' or
        '/\S+/\S+/\d{2}/\d+.shtml' or
        '/\S+/\S+/\d{4}/\d{2}/\d+.shtml'or
        '/\S+/\S+/\S+/\d{2}/\d+.shtml':
        SgccComCnNewsLoader
    }
