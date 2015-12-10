# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class CSDNNewsSpider(NewsSpider):

    u"""CSDN新闻爬虫"""

    name = 'csdn_net_news'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net']

    target_urls = [
        'article/\d{4}-\d{2}-\d{2}/\d+'
    ]

    title_xpath = '//h1[@class="title"]'
    content_xpath = '//div[@class="content"]/div[@class="left"]\
                     /div[@class="detail"]/div[@class="con news_content"]'
    author_xpath = '//*[@class="tit_bar"]'
    author_re = u'.*?作者\s*(\S+).*'
    publish_time_xpath = '//*[@class="tit_bar"]'
    publish_time_re = u'.*?发表于\s*(\d+-\d+-\d+ \d+:\d+|\S+).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="tit_bar"]'
    source_re = u'.*?来源\s*(\S+)\|.*'

    source_domain = 'csdn.net'
    source_name = 'CSDN'
