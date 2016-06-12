# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.spic_com_cn.spic_com_cn_news import(
    SpicComCnNewsLoader
)


class SpicComCnNewsSpider(LoaderMappingSpider):

    u"""国家电力投资集团公司新闻爬虫"""

    name = 'spic_com_cn_news'
    allowed_domains = ['spic.com.cn']
    start_urls = ['http://spic.com.cn/']

    mapping = {
        './\S+/\d{6}/t\d{8}_\d+.htm':
        SpicComCnNewsLoader
    }
