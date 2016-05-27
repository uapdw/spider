<<<<<<< HEAD
# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.mofcom_gov_cn.mofcom_gov_cn_news import(
    MofcomGovCnNewsLoader
)

class MofcomGovCnNewsSpider(LoaderMappingSpider):

    u"""中华人民共和国商务部新闻爬虫"""

    name = 'mofcom_gov_cn_news'
    allowed_domains = ['mofcom.gov.cn']
    start_urls = ['http://www.mofcom.gov.cn/']

    mapping = {
        'www.mofcom.gov.cn/article/ae/\S+/\d{6}/\d+.shtml':
        MofcomGovCnNewsLoader
    }
=======
# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.mofcom_gov_cn.mofcom_gov_cn_news import (
    MofcomGovCnNewsLoader
)


class MofcomGovCnNewsSpider(LoaderMappingSpider):

    u"""中华人民共和国商务部新闻爬虫"""

    name = 'mofcom_gov_cn_news'
    allowed_domains = ['mofcom.gov.cn']
    start_urls = ['http://www.mofcom.gov.cn/']

    mapping = {
        'article/.*?/\d+/\d+\.shtml':
        MofcomGovCnNewsLoader
    }
>>>>>>> 7057ade3e78625e3d0cf6e342ff2936b0b961005
