# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.zccct_com.zccct_com_news import (
    ZccctComNewsLoader
)


class ZccctComNewsSpider(LoaderMappingSpider):

    u"""株洲钻石切削刀具股份有限公司新闻爬虫"""

    name = 'zccct_com_news'
    allowed_domains = ['zccct.com']
    start_urls = ['http://www.zccct.com/']

    mapping = {
        'zccct\.com/html/\S+/\d{8}/\d+\.html':
        ZccctComNewsLoader
    }
