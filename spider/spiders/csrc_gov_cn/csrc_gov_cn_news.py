# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.csrc_gov_cn.csrc_gov_cn_news import(
    CsrcGovCnNewsLoader
)


class CsrcGovCnNewsSpider(LoaderMappingSpider):

    u"""中国证券监督管理委员会新闻爬虫"""

    name = 'csrc_gov_cn_news'
    allowed_domains = ['csrc.gov.cn']
    start_urls = ['http://www.csrc.gov.cn/pub/newsite/']

    mapping = {
        'www.csrc.gov.cn/pub/newsite/zjhxwfb/\S+/\d{6}/t\d{8}_\d+.html':
        CsrcGovCnNewsLoader
    }
