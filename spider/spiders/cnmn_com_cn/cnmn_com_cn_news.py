# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cnmn_com_cn.cnmn_com_cn_news import (
    CnmnComCnNewsLoader
)


class CnmnComCnNewsSpider(LoaderMappingSpider):

    u"""中国有色网新闻爬虫"""

    name = 'cnmn_com_cn_news'
    allowed_domains = ['cnmn.com.cn']
    start_urls = ['http://www.cnmn.com.cn/']

    mapping = {
        'cnmn\.com\.cn/ShowNews1\.aspx\?id=\d+': CnmnComCnNewsLoader
    }
