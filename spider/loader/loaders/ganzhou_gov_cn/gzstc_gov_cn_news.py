# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class GZStcNewsLoader(NewsLoader):

    u"""赣州市科技局"""


    title_xpath = '//*[@class="title"]'
    content_xpath = '//*[@id="articlebody"]'
    author_xpath = '//*[@class="info"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="info"]'
    publish_time_re = u'.*?时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="info"]'
    source_re = u'.*?来源：\s*(\S+).*?作者'

    source_domain = 'gzstc.gov.cn'
    source_name = u'赣州市科技局'
