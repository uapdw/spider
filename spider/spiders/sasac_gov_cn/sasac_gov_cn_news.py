# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.sasac_gov_cn.sasac_gov_cn_news import(
    SasacGovCnNewsLoader
)


class SasacGovCnNewsSpider(LoaderMappingSpider):

    u"""国务院国有资产监督管理委员会新闻爬虫"""

    name = 'sasac_gov_cn_news'
    allowed_domains = ['sasac.gov.cn']
    start_urls = ['http://www.sasac.gov.cn/']

    mapping = {
        'n\d+/n\d+/c\d+/content.html':
        SasacGovCnNewsLoader
    }
