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


class CnsandvikCut35ComNewsLoader(NewsLoader):

    u"""山特维克可乐满（中国）新闻"""

    title_xpath = '//*[@class="NewsTitle"]'
    content_xpath = '//*[@class="NContent"]'
    publish_time_xpath = '//*[@class="NewsDiv1"]'
    publish_time_re = u'.*?发布日期：(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    publish_time_format = '%Y-%m-%d %H:%M:%S'

    source_domain = 'cnsandvik.cut35.com'
    source_name = u'山特维克可乐满（中国）'
