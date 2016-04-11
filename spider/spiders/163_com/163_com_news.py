# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import WWW163NewsLoader


class WWW163NewsSpider(LoaderMappingSpider):

    u"""网易新闻爬虫"""

    name = '163_com_news'
    allowed_domains = ['www.163.com','news.163.com','money.163.com','ent.163.com','biz.163.com','tech.163.com']
    start_urls = ['http://www.163.com/']

    mapping = {
        '\S+\.163.com/\d{2}/\d{4}/\d+/\S+.html': WWW163NewsLoader
    }
