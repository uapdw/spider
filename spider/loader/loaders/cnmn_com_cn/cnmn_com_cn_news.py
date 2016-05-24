# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class CnmnComCnNewsLoader(NewsLoader):

    u"""中国有色网新闻"""

    title_xpath = '//*[@class="h4title"]'
    content_xpath = '//*[@id="txtcont"]'
    publish_time_xpath = '//*[@class="time"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日\s+(\d+:\d+)'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d-%H:%M'

    source_domain = 'cnmn.com.cn'
    source_name = u'中国有色网'
