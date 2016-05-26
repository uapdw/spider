# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.chalco_com_cn.chalco_com_cn_news import (
    ChalcoComCnNewsLoader
)


class ChalcoComCnNewSpider(LoaderMappingSpider):

    u"""中国铝业公司新闻爬虫"""

    name = 'chalco_com_cn_news'
    allowed_domains = [
        'chalco.com.cn'
    ]
    start_urls = ['http://www.chalco.com.cn/zgly/index.htm']

    mapping = {
        'chalco\.com\.cn/.*?/webinfo/\d{4}/\d{2}/\d+\.htm':
        ChalcoComCnNewsLoader
    }
