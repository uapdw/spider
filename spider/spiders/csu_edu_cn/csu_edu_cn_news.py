# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.csu_edu_cn.csu_edu_cn_news import (
    CsuEduCnNewsLoader
)


class CsuEduCnNewsSpider(LoaderMappingSpider):

    u"""中南大学新闻爬虫"""

    name = 'csu_edu_cn'
    allowed_domains = [
        'csu.edu.cn'
    ]
    start_urls = [
        'http://www.csu.edu.cn/'
    ]

    mapping = {
        'csu\.edu\.cn/info/\d+/\d+\.htm': CsuEduCnNewsLoader
    }
