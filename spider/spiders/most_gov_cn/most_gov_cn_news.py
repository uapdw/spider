# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.most_gov_cn.most_gov_cn_news import(
    MostGovCnNewsLoader
)

class MostGovCnNewsSpider(LoaderMappingSpider):

    u"""中华人民共和国科学技术部新闻爬虫"""

    name = 'most_gov_cn_news'
    allowed_domains = ['most.gov.cn']
    start_urls = ['http://www.most.gov.cn/']

    mapping = {
        'most.gov.cn/\S+/\S+/\S+/\d{6}/t\d{8}_\d+.htm' or
	'most.gov.cn/\S+/\d{6}/t\d{8}_\d+.htm':
        MostGovCnNewsLoader
    }
