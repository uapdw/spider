# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.china5e_com.china5e_com_news import(
    China5eComNewsLoader
)


class China5eComNewsSpider(LoaderMappingSpider):

    u"""中国能源网新闻爬虫"""

    name = 'china5e_com_news'
    allowed_domains = ['china5e.com']
    start_urls = ['http://www.china5e.com/news/']

    mapping = {
        'www.china5e.com/news/news-\d+-\d+.html':
        China5eComNewsLoader
    }
