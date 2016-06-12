# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.dqzyxy_net.ltxzgglzx_dqzyxy_net_news import(
    LtxzgglzxDqzyxyNetNewsLoader
)


class LtxzgglzxDqzyxyNetNewsSpider(LoaderMappingSpider):

    u"""大庆职业学院离退休职工管理中心新闻爬虫"""

    name = 'ltxzgglzx_dqzyxy_net_news'
    allowed_domains = ['dqzyxy.net']
    start_urls = ['http://www.dqzyxy.net/Category_198/Index.aspx']

    mapping = {
        '/Item/\d+.aspx':
        LtxzgglzxDqzyxyNetNewsLoader
    }
