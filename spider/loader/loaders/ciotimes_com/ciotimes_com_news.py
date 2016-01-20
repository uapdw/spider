# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class CiotimesNewsLoader(NewsLoader):

    u"""CIO时代新闻爬虫"""

    name = 'ciotimes_com_news'
    allowed_domains = ['ciotimes.com']
    start_urls = ['http://www.ciotimes.com/']

    target_urls = [
        'ciotimes\.com/\S+/\d+\.html'
    ]

    title_xpath = '//*[contains(@class, "zw")]/h4[1]'
    content_xpath = '//*[contains(@class, "zw")]'
    publish_time_xpath = '//*[contains(@class, "ly")]'
    publish_time_re = '.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[contains(@class, "ly")]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'ciotimes.com'
    source_name = u'CIO时代'
