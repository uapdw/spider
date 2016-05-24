# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.jxysdzkcj_gov_cn.jxysdzkcj_gov_cn_news import (
    JxysdzkcjGovCnNewsLoader
)


class JxysdzkcjGovCnNewsSpider(LoaderMappingSpider):

    u"""江西有色地质勘查局新闻爬虫"""

    name = 'jxysdzkcj_gov_cn_news'
    allowed_domains = ['jxysdzkcj.gov.cn']
    start_urls = ['http://www.jxysdzkcj.gov.cn/']

    mapping = {
        'jxysdzkcj\.gov\.cn/news_detail/newsId=\d+\.html':
        JxysdzkcjGovCnNewsLoader
    }
