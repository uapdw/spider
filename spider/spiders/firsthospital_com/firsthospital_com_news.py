# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.firsthospital_com.firsthospital_com_news import(
    FirsthospitalComNewsLoader
)


class FirsthospitalComNewsSpider(LoaderMappingSpider):

    u"""大庆油田总医院新闻爬虫"""

    name = 'firsthospital_com_news'
    allowed_domains = ['first-hospital.com']
    start_urls = ['http://www.first-hospital.com/']

    mapping = {
        'bread.asp\?fileid=\d+':
        FirsthospitalComNewsLoader
    }
