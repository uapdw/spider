# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.chinania_org_cn.chinania_org_cn_news import (
    ChinaniaOrgCnNewsLoader
)


class ChinaniaOrgCnNewsSpider(LoaderMappingSpider):

    u"""中国有色金属工业协会新闻爬虫"""

    name = 'chinania_org_cn_news'
    allowed_domains = ['chinania.org.cn']
    start_urls = ['http://www.chinania.org.cn/']

    mapping = {
        'chinania\.org\.cn/html/\S+/\d{4}/\d{4}/\d+\.html':
        ChinaniaOrgCnNewsLoader
    }
