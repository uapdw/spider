# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.bjx_com_cn.bjx_com_cn_news import(
    BjxComCnNewsLoader
)


class BjxComCnNewsSpider(LoaderMappingSpider):

    u"""北极星电力网新闻爬虫"""

    name = 'bjx_com_cn_news'
    allowed_domains = ['bjx.com.cn']
    start_urls = ['http://www.bjx.com.cn/']

    mapping = {
        'news.bjx.com.cn/html/\d{8}/\d+.shtml':
        BjxComCnNewsLoader
    }
