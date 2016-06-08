# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.sinopecnews_com_cn.sinopecnews_com_cn_news import(
    SinopecnewsComCnNewsLoader
)


class SinopecnewsComCnNewsSpider(LoaderMappingSpider):

    u"""中国石化新闻网新闻爬虫"""

    name = 'sinopecnews_com_cn_news'
    allowed_domains = ['sinopecnews.com.cn']
    start_urls = ['http://www.sinopecnews.com.cn/shnews/node_11316.htm']

    mapping = {
        '../news/content/\d{4}-\d{2}/\d{2}/content_\d+.htm':
        SinopecnewsComCnNewsLoader
    }
