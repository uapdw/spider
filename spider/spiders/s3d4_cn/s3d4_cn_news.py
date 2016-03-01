# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import S3d4NewsLoader


class S3d4NewsSpider(LoaderMappingSpider):

    u"""说三道四新闻爬虫"""

    name = 's3d4_cn_news'
    allowed_domains = ['s3d4.cn']
    start_urls = ['http://s3d4.cn/']

    mapping = {
        's3d4\.cn/news/\d+': S3d4NewsLoader
    }
