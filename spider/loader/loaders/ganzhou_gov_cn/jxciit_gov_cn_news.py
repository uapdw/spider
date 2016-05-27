# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JXCiitNewsLoader(NewsLoader):

    u"""江西省工信部爬虫"""


    title_xpath = '//title'
    content_xpath = '//*[@id="fontzoom"]'
    author_xpath = '//*[@height="55"]'
    author_re = u'.*?作者：\s*(\S+)】.*'
    publish_time_xpath = '//*[@height="55"]'
    publish_time_re = u'.*?发布时间：\s*(\d{4})年(\d{1,2})月(\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@height="55"]'
    source_re = u'.*?来源：\s*(\S+)】.*'

    source_domain = 'jxciit.gov.cn'
    source_name = u'江西省工信部'