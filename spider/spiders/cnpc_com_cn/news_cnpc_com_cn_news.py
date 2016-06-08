# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.cnpc_com_cn.news_cnpc_com_cn_news import(
    NewsCnpcComCnNewsLoader
)


class NewsCnpcComCnNewsSpider(LoaderMappingSpider):

    u"""中国石油新闻中心新闻爬虫"""

    name = 'news_cnpc_com_cn_news'
    allowed_domains = ['cnpc.com.cn']
    start_urls = ['http://news.cnpc.com.cn/']

    mapping = {
        'news.cnpc.com.cn/system/\d{4}/\d{2}/\d{2}/\d+.shtml':
        NewsCnpcComCnNewsLoader
    }
