# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.mohrss_gov_cn.mohrss_gov_cn_news import(
    MohrssGovCnNewsLoader
)

class MohrssGovCnNewsSpider(LoaderMappingSpider):

    u"""中华人民共和国人力资源和社会保障部新闻爬虫"""

    name = 'mohrss_gov_cn_news'
    allowed_domains = ['mohrss.gov.cn']
    start_urls = ['http://www.mohrss.gov.cn/']

    mapping = {
        'www.mohrss.gov.cn/SYrlzyhshbzb/dongtaixinwen/buneiyaowen/\d{6}/t\d{8}_\d+.html':
        MohrssGovCnNewsLoader
    }
