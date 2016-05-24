# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class N10jqkaComCnNewsLoader(NewsLoader):

    u"""同花顺财经新闻"""

    title_xpath = '//*[@class="atc-head"]'
    content_xpath = '//*[@class="atc-content"]'
    publish_time_xpath = '//*[@class="time"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'

    source_domain = '10jqka.com.cn'
    source_name = u'同花顺财经'
