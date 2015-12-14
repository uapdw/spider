# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class QudongNewsSpider(NewsSpider):

    u"""驱动中国新闻爬虫"""

    name = 'qudong_com_news'
    allowed_domains = ['qudong.com']
    start_urls = ['http://www.qudong.com/']

    target_urls = [
        'qudong\.com/\d{4}/\d{4}/\d+\.shtml'
    ]

    title_xpath = '//*[@class="art-hd"]/h1'
    content_xpath = '//*[@class="content"]'
    publish_time_xpath = '//*[@id="pubtime"]'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="art-hd"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'qudong.com'
    source_name = u'驱动中国'
