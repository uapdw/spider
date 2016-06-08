# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.sinoergy_com.sinoergy_com_news import(
    SinoergyComNewsLoader
)


class SinoergyComNewsSpider(LoaderMappingSpider):

    u"""华夏能源网新闻爬虫"""

    name = 'sinoergy_com_news'
    allowed_domains = ['sinoergy.com']
    start_urls = ['http://www.sinoergy.com/']

    mapping = {
        'www.sinoergy.com/\S+/\d+/':
        SinoergyComNewsLoader
    }
