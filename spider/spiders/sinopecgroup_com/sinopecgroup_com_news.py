# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.sinopecgroup_com.sinopecgroup_com_news import(
    SinopecgroupComNewsLoader
)


class SinopecgroupComNewsSpider(LoaderMappingSpider):

    u"""中国石化新闻爬虫"""

    name = 'sinopecgroup_com_news'
    allowed_domains = ['sinopecgroup.com']
    start_urls = ['http://www.sinopecgroup.com/group/']

    mapping = {
        '/group/\S+/\S+/\d{8}/news_\d{8}_\d+.shtml':
        SinopecgroupComNewsLoader
    }
