# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.jxtc_com_cn.jxtc_com_cn_news import (
    JxtcComCnNewsLoader
)


class JxtcComCnNewSpider(LoaderMappingSpider):

    u"""江钨集团新闻爬虫"""

    name = 'jxtc_com_cn_news'
    allowed_domains = [
        'jxtc.com.cn'
    ]
    start_urls = ['http://www.jxtc.com.cn/']

    mapping = {
        'jxtc\.com\.cn/\S+/\d{8}/jwjt\S+\.html': JxtcComCnNewsLoader
    }
