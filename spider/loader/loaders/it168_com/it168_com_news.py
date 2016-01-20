# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class It168NewsLoader(NewsLoader):

    u"""It168新闻爬虫"""

    name = 'it168_com_news'
    allowed_domains = ['it168.com']
    start_urls = ['http://www.it168.com/']

    target_urls = [
        'it168\.com/a\d{4}/\d{4}/\d+/\d+\.shtml'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@id="detailWord"]'
    author_xpath = '//*[@class="time"]'
    author_re = u'.*?作者:\s*(\S+).*'
    publish_time_xpath = '//*[@class="time"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="time"]'
    source_re = u'.*?\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}\s*(\S+).*'

    source_domain = 'it168.com'
    source_name = 'It168'
