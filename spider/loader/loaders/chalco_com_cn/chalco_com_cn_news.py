# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class ChalcoComCnNewsLoader(NewsLoader):

    u"""中国铝业公司新闻"""

    title_xpath = '//*[@class="content-title"]'
    content_xpath = '//*[@class="content-con"]'
    publish_time_xpath = '//*[@class="content-info"]'
    publish_time_re = u'.*?来源：\s*\S*\s*时间：\s*(\d{4}-\d{2}-\d{2})'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="content-info"]'
    source_re = u'.*?来源：\s*(\S*)\s*时间：\s*\d{4}-\d{2}-\d{2}'

    source_domain = 'chalco.com.cn'
    source_name = u'中国铝业公司'
