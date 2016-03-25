# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import ENorthNewsLoader


class ENorthNewsSpider(LoaderMappingSpider):
    '''北方网新闻爬虫'''

    name = 'enorth_com_cn_news'
    allowed_domains = [
        'economy.enorth.com.cn',
        'tianjin.enorth.com.cn',
        'news.enorth.com.cn',
        'it.enorth.com.cn',
    ]
    start_urls = ['http://www.enorth.com.cn/']

    mapping = {
        '\w+\.enorth.com.cn/\w+/\d{4}/\d{2}/\d{2}/|w+.shtml': ENorthNewsLoader
    }
