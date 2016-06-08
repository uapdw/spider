# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cnooc_com_cn.cnooc_com_cn_news import(
    CnoocComCnNewsLoader
)


class CnoocComCnNewsSpider(LoaderMappingSpider):

    u"""中国海油新闻爬虫"""

    name = 'cnooc_com_cn_news'
    allowed_domains = ['cnooc.com.cn']
    start_urls = ['http://www.cnooc.com.cn/']

    mapping = {
        'www.cnooc.com.cn/art/\d{4}/\d+/\d+/art_\d+_\d+.html':
        CnoocComCnNewsLoader
    }
