# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.miit_gov_cn.miit_gov_cn_news import(
    MiitGovCnNewsLoader
)

class MiitGovCnNewsSpider(LoaderMappingSpider):

    u"""中华人民共和国工业和信息化部新闻爬虫"""

    name = 'miit_gov_cn_news'
    allowed_domains = [
	'miit.gov.cn'
    ]
    start_urls = ['http://www.miit.gov.cn/newweb/index.html']

    mapping = {
	'www.miit.gov.cn/newweb/n\d+/n\d+/n\d+/c\d+/content.html':
	MiitGovCnNewsLoader
    }
