# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import SPNComNewsLoader


class SPNComNewsSpider(LoaderMappingSpider):

    u"""睿商在线新闻爬虫"""

    name = 'spn_com_cn_news'
    allowed_domains = ['spn.com.cn']
    start_urls = ['http://www.spn.com.cn/']

    mapping = {
        'http://www.spn.com.cn/\w+/\d+/\d+.html': SPNComNewsLoader
    }
