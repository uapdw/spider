# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import GZJxgttNewsLoader


class GZJxgttNewsSpider(LoaderMappingSpider):
    '''赣州市国土资源局爬虫'''

    name = 'gz_jxgtt_gov_cn_news'
    allowed_domains = [
        'gz.jxgtt.gov.cn',
    ]
    start_urls = ['http://gz.jxgtt.gov.cn/Index.shtml']

    mapping = {
        'News.shtml?\?p5=\d+&col=\d+': GZJxgttNewsLoader
    }