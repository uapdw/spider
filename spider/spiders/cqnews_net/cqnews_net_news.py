# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class CqNewsNetNewsSpider(NewsSpider):

    u"""华龙网新闻爬虫"""

    name = 'cqnews_net_news'
    allowed_domains = ['cqnews.net']
    start_urls = ['http://www.cqnews.net/']

    target_urls = [
        'cq\.cqnews\.net/\S+/\d{4}-\d{2}/\d{2}/content_\d+.htm'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@id="main_text"]'
    publish_time_xpath = '//*[@class="jiange3"][1]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="jiange3"][2]/a'

    source_domain = 'cqnews.net'
    source_name = u'华龙网'
