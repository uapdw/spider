# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class MiitGovCnNewsLoader(NewsLoader):

    u"""中华人民共和国工业和信息化部新闻"""

    title_xpath = '//*[@id="con_title"]'
    content_xpath = '//*[@class="ccontent center"]'
#    author_xpath = ''

    publish_time_xpath = '//*[@id="con_time"]'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="cinfo center"]'
    source_re = u'.*?来源：\s*(\S+)'

    source_domain = 'miit.gov.cn'
    source_name = u'中华人民共和国工业和信息化部'
