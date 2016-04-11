# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import TechwebNewsLoader


class TechwebNewsSpider(LoaderMappingSpider):

    u"""TechWeb新闻爬虫"""

    name = 'techweb_com_cn_news'
    allowed_domains = [
        'people.techweb.com.cn',
        'mi.techweb.com.cn',
        'tech.techweb.com.cn',
        'www.techweb.com.cn',
    ]
    start_urls = ['http://www.techweb.com.cn/']

    mapping = {
        'www\.techweb\.com\.cn/\S+/\d{4}-\d{2}-\d{2}/\d+\.shtml':
        TechwebNewsLoader
    }
