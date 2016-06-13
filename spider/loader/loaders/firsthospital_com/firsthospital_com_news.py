# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class FirsthospitalComNewsLoader(NewsLoader):

    u"""大庆油田总医院新闻"""

    title_xpath = '//*[@class="dh2"]'
    content_xpath = '//*[@class="dh7"]'

    publish_time_xpath = '//*[@class="dh4"]'
    publish_time_re = u'.*(\d{4}-\d{1,2}-\d{1,2}).*'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'first-hospital.com'
    source_name = u'大庆油田总医院'
