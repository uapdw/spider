# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import IFengNewsLoader


class IFengNewsSpider(LoaderMappingSpider):

    u"""凤凰新闻爬虫"""

    name = 'ifeng_com_news'
    allowed_domains = [
        'news.ifeng.com',
        'finance.ifeng.com',
        'tech.ifeng.com',
    ]
    start_urls = ['http://www.ifeng.com']

    mapping = {
        'ifeng\.com/\S+?/\d{8}/\d+_\d{1}.shtml': IFengNewsLoader,
        'ifeng\.com/\S+?/\d{4}/\d{4}/\d+.shtml': IFengNewsLoader
    }
