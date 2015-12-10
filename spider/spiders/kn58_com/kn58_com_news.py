# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class Kn58NewsSpider(NewsSpider):

    u"""微客网新闻爬虫"""

    name = 'kn58_com_news'
    allowed_domains = ['kn58.com']
    start_urls = ['http://www.kn58.com/']

    target_urls = [
        'kn58\.com/.*/detail_\d{4}_\d{4}/\d+\.html'
    ]

    title_xpath = '//*[@class="title"]/h1'
    content_xpath = '//*[@class="left"]'
    publish_time_xpath = '//*[@class="titiefu"]'
    publish_time_re = '.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="titiefu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'kn58.com'
    source_name = u'微客网'
