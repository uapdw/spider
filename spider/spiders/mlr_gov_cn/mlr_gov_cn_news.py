# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.mlr_gov_cn.mlr_gov_cn_news import(
    MlrGovCnNewsLoader
)


class Spider(LoaderMappingSpider):

    u"""中华人民共和国国土资源部新闻爬虫"""

    name = 'mlr_gov_cn_news'
    allowed_domains = [
        'mlr.gov.cn'
    ]
    start_urls = ['http://news.mlr.gov.cn/']

    mapping = {
        'news.mlr.gov.cn/jrxw/\d{6}/t\d{8}_\d+.htm':
        MlrGovCnNewsLoader
    }
