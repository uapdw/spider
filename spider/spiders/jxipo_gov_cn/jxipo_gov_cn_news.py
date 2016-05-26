# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.jxipo_gov_cn.jxipo_gov_cn_news import (
    JxipoGovCnNewsLoader
)


class JxipoGovCnNewsSpider(LoaderMappingSpider):

    u"""江西省知识产权局新闻爬虫"""

    name = 'jxipo_gov_cn_news'
    allowed_domains = [
        'jxipo.gov.cn'
    ]
    start_urls = [
        'http://www.jxipo.gov.cn/'
    ]

    mapping = {
        'jxipo\.gov\.cn/1/\d+\.aspx':
        JxipoGovCnNewsLoader
    }
