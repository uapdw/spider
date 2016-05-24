# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class ChinanfmiComNewsLoader(NewsLoader):

    u"""中国矿冶设备供求网新闻爬虫"""

    title_xpath = '//*[@class="title"]'
    content_xpath = '//*[@class="content"]'
    publish_time_xpath = '//*[@class="info"]'
    publish_time_re = u'.*?发布日期：\s*(\d{4}-\d{2}-\d{2})'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'chinanfmi.com'
    source_name = u'中国矿冶设备供求网'
