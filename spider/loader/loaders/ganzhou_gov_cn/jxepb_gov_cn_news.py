# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JXEpbNewsLoader(NewsLoader):

    u"""江西省环境保护厅爬虫"""


    title_xpath = '//*[@class="tzhj"]'
    content_xpath = '//*[@id="Content"]'
    author_xpath = '//*[@height="30"]'
    author_re = u'.*?责任编辑：\s*(\S+).*'
    publish_time_xpath = '//*[@class="tzhj3"]'
    publish_time_re = u'.*?日期： \s*(\d{4}-\d{1,2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="tzhj3"]'
    source_re = u'.*?稿源：\s*(\S+).*'

    source_domain = 'jxepb.gov.cn'
    source_name = u'江西省环境保护厅'