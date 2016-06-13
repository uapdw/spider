# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.chng_com_cn.chng_com_cn_news import(
    ChngComCnNewsLoader
)


class ChngComCnNewsSpider(LoaderMappingSpider):

    u"""中国华能集团公司新闻爬虫"""

    name = 'chng_com_cn_news'
    allowed_domains = ['chng.com.cn']
    start_urls = ['http://www.chng.com.cn/']

    mapping = {
        'n\d+/n\d+/c\d+/content.html':
        ChngComCnNewsLoader
    }
