# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.jxgtt_gov_cn.jxgtt_gov_cn_news import (
    JxgttGovCnNewsLoader
)


class JxgttGovCnNewsSpider(LoaderMappingSpider):

    u"""江西省国土资源厅新闻爬虫"""

    name = 'jxgtt_gov_cn_news'
    allowed_domains = ['jxgtt.gov.cn']
    start_urls = ['http://www.jxgtt.gov.cn/Index.shtml']

    mapping = {
        'jxgtt\.gov\.cn/News\.shtml\?p5=\d+&col=\d+':
        JxgttGovCnNewsLoader
    }
