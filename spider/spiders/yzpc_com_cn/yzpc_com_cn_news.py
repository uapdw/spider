# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.yzpc_com_cn.yzpc_com_cn_news import(
    YzpcComCnNewsLoader
)


class YzpcComCnNewsSpider(LoaderMappingSpider):

    u"""长江石化新闻爬虫"""

    name = 'yzpc_com_cn_news'
    allowed_domains = ['yzpc.com.cn']
    start_urls = ['http://www.yzpc.com.cn/']

    mapping = {
        'www.yzpc.com.cn/\S+/news\d+.html':
        YzpcComCnNewsLoader
    }
