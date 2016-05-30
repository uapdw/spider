# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.winwelltungsten_com.winwelltungsten_com_news import(
    WinwelltungstenComNewsLoader
)


class WinwelltungstenComNewsSpider(LoaderMappingSpider):

    u"""钨业在线新闻爬虫"""

    name = 'winwelltungsten_com_news'
    allowed_domains = ['winwelltungsten.com']
    start_urls = ['http://www.winwelltungsten.com/']

    mapping = {
        '/html/yaowen/\S+/\d{4}/\d{4}/\d+\.html'or
        '/html/zixun/\S+/\d{4}/\d{4}/\d+\.html':
        WinwelltungstenComNewsLoader
    }
