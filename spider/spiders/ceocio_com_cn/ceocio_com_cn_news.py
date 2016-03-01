# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CeocioNewsLoader


class CeocioNewsSpider(LoaderMappingSpider):

    u"""经理世界网新闻爬虫"""

    name = 'ceocio_com_cn_news'
    allowed_domains = ['ceocio.com.cn']
    start_urls = ['http://www.ceocio.com.cn/']

    mapping = {
        'ceocio\.com\.cn/.*/\d{4}-\d{2}-\d{2}/\d+\.shtml': CeocioNewsLoader
    }
