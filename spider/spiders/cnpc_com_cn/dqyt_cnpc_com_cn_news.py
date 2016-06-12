# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cnpc_com_cn.dqyt_cnpc_com_cn_news import(
    DqytCnpcComCnNewsLoader
)


class DqytCnpcComCnNewsSpider(LoaderMappingSpider):

    u"""中国石油大庆油田新闻爬虫"""

    name = 'dqyt_cnpc_com_cn_news'
    allowed_domains = ['dqyt.cnpc.com.cn']
    start_urls = ['http://dqyt.cnpc.com.cn/']

    mapping = {
        '../dq/\S+/\d{6}/\S+.shtml':
        DqytCnpcComCnNewsLoader
    }
