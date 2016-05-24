# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.people_com_cn.people_com_cn_news import (
    N1PeopleComCnNewsLoader
)


class CpcPeopleComCnNewsSpider(LoaderMappingSpider):

    u"""中国共产党新闻网新闻爬虫"""

    name = 'cpc_people_com_cn_news'
    allowed_domains = ['people.com.cn']
    start_urls = ['http://cpc.people.com.cn/']

    mapping = {
        'people\.com\.cn/.*?/n1/\d{4}/\d{4}/c\d+-\d+.html':
        N1PeopleComCnNewsLoader
    }
