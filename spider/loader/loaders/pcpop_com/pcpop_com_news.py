# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class PcpopNewsLoader(NewsLoader):

    u"""泡泡网新闻爬虫"""

    name = 'pcpop_com_news'
    allowed_domains = ['pcpop.com']
    start_urls = ['http://www.pcpop.com/']

    target_urls = [
        'pcpop\.com/doc/\d+/\d+/\d+\.shtml'
    ]

    title_xpath = '//*[@class="l1"]/h1'
    content_xpath = '//*[@class="main"]'
    author_xpath = '//*[@class="chuchu"]'
    author_re = u'.*?作者:\s*(\S+).*'
    publish_time_xpath = '//*[@class="chuchu"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日\s*(\d{2}:\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d-%H:%M'
    source_xpath = '//*[@class="chuchu"]'
    source_re = u'.*?出处：\s*(\S+).*'

    source_domain = 'pcpop.com'
    source_name = u'泡泡网'
