# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import SinaNewsLoader


class SinaNewsSpider(LoaderMappingSpider):

    u"""新浪新闻爬虫"""

    name = 'sina_com_cn_news'
    allowed_domains = [
        'news.sina.com.cn',
        'finance.sina.com.cn',
        'tech.sina.com.cn',
    ]
    start_urls = ['http://www.sina.com.cn']

    mapping = {
        '.*?sina\.com\.cn/\S+?/\d{4}-\d{2}-\d{2}/doc-\S+\.shtml':
        SinaNewsLoader,
        '.*?sina\.com\.cn/\d{4}-\d{2}-\d{2}/\d+.html': SinaNewsLoader,
        '.*?sina\.com\.cn/\S+?/\d{8}/\d+\.shtml': SinaNewsLoader
    }
