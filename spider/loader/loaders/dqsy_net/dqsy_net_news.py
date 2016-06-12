# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class DqsyNetNewsLoader(NewsLoader):

    u"""大庆师范学院新闻"""

    title_xpath = '//*[@class="titlestyle48503"]'
    content_xpath = '//*[@id="vsb_content_1004"]'

    publish_time_xpath = '//*[@class="timestyle48503"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'dqsy.net'
    source_name = u'大庆师范学院'
