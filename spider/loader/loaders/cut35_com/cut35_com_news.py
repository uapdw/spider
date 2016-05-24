# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class Cut35ComNewsLoader(NewsLoader):

    u"""中国刀具商务网新闻"""

    title_xpath = '//*[@class="NS_T"]/h1'
    content_xpath = '//*[@class="NContent"]'
    publish_time_xpath = '//*[@class="NS_T1"]'
    publish_time_re = u'.*?日期:\s*(\d{4}-\d{2}-\d{2}).*?来源：\s*\S+'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="NS_T1"]'
    source_re = u'.*?日期:\s*\d{4}-\d{2}-\d{2}.*?来源：\s*(\S+)'

    source_domain = 'cut35.com'
    source_name = u'中国刀具商务网'
