# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class OmetalComNewsLoader(NewsLoader):

    u"""全球金属网新闻"""

    title_xpath = '//h1'
    content_xpath = '//*[@class="font105pt"]'
    publish_time_xpath = '//*[@class="font9pt"]'
    publish_time_re = u'.*?(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})'
    publish_time_format = '%Y-%m-%d %H:%M:%S'

    source_domain = 'ometal.com'
    source_name = u'全球金属网'
