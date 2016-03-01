# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import CSDNBlogLoader


class CSDNBlogSpider(LoaderMappingSpider):

    u"""CSDN博客爬虫"""

    name = 'csdn_net_blog'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net']

    mapping = {
        'http://blog.csdn.net/\S+?/article/details/\d+': CSDNBlogLoader
    }
