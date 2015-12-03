# -*- coding: utf-8 -*-

from spider.spiders.base_spider import SimpleNewsSpider


class CSDNNewsSpider(SimpleNewsSpider):

    name = 'csdn_net_news'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net']

    target_urls = [
        'article/\d{4}-\d{2}-\d{2}/\d+'
    ]

    title_xpath = '//h1[@class="title"]'
