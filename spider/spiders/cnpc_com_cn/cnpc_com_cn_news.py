# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cnpc_com_cn.cnpc_com_cn_news import(
    CnpcComCnNewsLoader
)


class CnpcComCnNewsSpider(LoaderMappingSpider):

    u"""中国石油新闻爬虫"""

    name = 'cnpc_com_cn_news'
    allowed_domains = ['cnpc.com.cn']
    start_urls = ['http://www.cnpc.com.cn/cnpc/index.shtml']

    mapping = {
        '../cnpc/\S+/\d{6}/\S+.shtml':
        CnpcComCnNewsLoader
    }
