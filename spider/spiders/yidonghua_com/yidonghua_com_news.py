# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import YidonghuaNewsLoader


class YidonghuaNewsSpider(LoaderMappingSpider):

    u"""移动信息化新闻爬虫"""

    name = 'yidonghua_com_news'
    allowed_domains = ['yidonghua.com']
    start_urls = ['http://www.yidonghua.com']

    mapping = {
        'yidonghua\.com/post/\d+\.html': YidonghuaNewsLoader
    }
