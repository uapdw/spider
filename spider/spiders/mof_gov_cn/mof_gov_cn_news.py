# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.mof_gov_cn.mof_gov_cn_news import(
    MofGovCnNewsLoader
)

class MofGovCnNewsSpider(LoaderMappingSpider):

    u"""中华人民共和国财政部新闻爬虫"""

    name = 'mof_gov_cn_news'
    allowed_domains = ['mof.gov.cn']
    start_urls = ['http://www.mof.gov.cn/index.htm']

    mapping = {
        '\S+.mof.gov.cn/\S+/\S+/\d{6}/t\d{8}_\d+.htm':
        MofGovCnNewsLoader
    }
