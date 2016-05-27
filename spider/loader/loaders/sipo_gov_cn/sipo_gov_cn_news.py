# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class SipoGovCnNewsLoader(NewsLoader):

    u"""国家知识产权局新闻"""

    title_xpath = '//*[@class="index_title"]'
    content_xpath = '//*[@class="index_art_con"]'
    publish_time_xpath = '//*[@class="index_time"]'
    publish_time_re = u'.*?发布时间：(\d{4}-\d{1,2}-\d{1,2})'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'sipo.gov.cn'
    source_name = u'国家知识产权局'
