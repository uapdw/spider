# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class CnpcComCnNewsLoader(NewsLoader):

    u"""中国石油新闻"""

    title_xpath = '//*[@class="content-l1"]/h1[1]'
    content_xpath = '//*[@class="content-l2-l-text"]'

    publish_time_xpath = '//*[@class="date"]'
    publish_time_re = u'.*(\d{4})/(\d{2})/(\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@id="laiyuan"]'

    source_domain = 'cnpc.com.cn'
    source_name = u'中国石油'
