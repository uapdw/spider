# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.news_smm_cn.news_smm_cn_news import (
    NewsSmmCnNewsLoader
)


class NewsSmmCnSpider(LoaderMappingSpider):

    u"""上海有色网新闻爬虫"""

    name = 'news_smm_cn_news'
    allowed_domains = ['news.smm.cn']
    start_urls = ['http://news.smm.cn/']

    mapping = {
        'news\.smm\.cn/r/\d{4}-\d{2}-\d{2}/\d+\.html': NewsSmmCnNewsLoader
    }
