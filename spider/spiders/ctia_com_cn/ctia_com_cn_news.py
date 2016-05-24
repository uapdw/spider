# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.ctia_com_cn.ctia_com_cn_news import (
    CtiaComCnNewsLoader
)


class CtiaComCnNewsSpider(LoaderMappingSpider):

    u"""中国钨业协会新闻爬虫"""

    name = 'ctia_com_cn_news'
    allowed_domains = ['ctia.com.cn']
    start_urls = ['http://www.ctia.com.cn/']

    mapping = {
        'ctia\.com\.cn/Article/\d{4}/\d+\.html': CtiaComCnNewsLoader
    }
