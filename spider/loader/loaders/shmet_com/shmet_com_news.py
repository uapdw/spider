# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class ShmetComNewsLoader(NewsLoader):

    u"""上海金属网新闻"""

    title_xpath = '//*[@class="tn-title"]'
    content_xpath = '//*[@class="tn-detail-text"]'
    publish_time_xpath = '//*[@class="tn-date"]'
    publish_time_format = '%Y-%m-%d %H:%M'

    source_domain = 'shmet.com'
    source_name = u'上海金属网'
