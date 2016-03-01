# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import ZJOLComCnNewsLoader


class ZJOLComCnNewsSpider(LoaderMappingSpider):
    '''浙江在线新闻爬虫'''

    name = 'zjol_com_cn_news'
    allowed_domains = ['zjol.com.cn']
    start_urls = ['http://www.zjol.com.cn/']

    mapping = {
        '\w+\.zjol.com.cn/\w+/\d{4}/\d{2}/\d{2}/\d+.shtml': ZJOLComCnNewsLoader
    }
