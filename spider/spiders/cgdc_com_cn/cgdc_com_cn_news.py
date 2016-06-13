# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cgdc_com_cn.cgdc_com_cn_news import(
    CgdcComCnNewsLoader
)


class CgdcComCnNewsSpider(LoaderMappingSpider):

    u"""中国国电集团公司新闻爬虫"""

    name = 'cgdc_com_cn_news'
    allowed_domains = ['cgdc.com.cn']
    start_urls = ['http://www.cgdc.com.cn/']

    mapping = {
        '/\S+/\d+.jhtml':
        CgdcComCnNewsLoader
    }
