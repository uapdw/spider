# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.jxstc_gov_cn.jxstc_gov_cn_news import (
    JxstcGovCnNewsLoader
)


class JxstcGovCnNewSpider(LoaderMappingSpider):

    u"""江西省科学技术厅新闻爬虫"""

    name = 'jxstc_gov_cn_news'
    allowed_domains = [
        'jxstc.gov.cn'
    ]
    start_urls = ['http://www.jxstc.gov.cn/']

    mapping = {
        'jxstc\.gov\.cn/ReadNews\.asp\?NewsID=\d+':
        JxstcGovCnNewsLoader
    }
