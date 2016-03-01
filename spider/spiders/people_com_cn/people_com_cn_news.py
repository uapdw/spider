# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import PeopleComCnNewsLoader


class PeopleComCnNewsSpider(LoaderMappingSpider):

    u"""人民网新闻爬虫"""

    name = 'people_com_cn_news'
    allowed_domains = ['people.com.cn']
    start_urls = ['http://www.people.com.cn/']

    mapping = {
        'people\.com\.cn/n/\d{4}/\d{4}/c\d+-\d+.html': PeopleComCnNewsLoader
    }
