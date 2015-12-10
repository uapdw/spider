# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class ChinabyteNewsSpider(NewsSpider):

    u"""搜狐新闻爬虫"""

    name = 'chinabyte_com_news'
    allowed_domains = ['chinabyte.com']
    start_urls = ['http://chinabyte.com/']

    target_urls = [
        'chinabyte\.com/\d+/\d+\.shtml'
    ]

    title_xpath = '//*[@id="artibodyTitle"]'
    content_xpath = '//*[@id="main-article"]'
    author_xpath = '//*[@class="auth"]'
    publish_time_xpath = '//*[@class="date"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="where"]'

    source_domain = 'chinabyte.com'
    source_name = u'比特网'
