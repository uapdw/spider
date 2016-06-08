# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class CmenCcNewsLoader(NewsLoader):

    u"""国家能源网新闻"""

    title_xpath = '//*[@class="txt-con clear top-padding2"]/h2'
    content_xpath = '//*[@class="all-txt"]'

    publish_time_xpath = '//*[@class="txt-con clear top-padding2"]'
    publish_time_re = u'.*?发表时间：\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d %H:%M:%S'

    source_xpath = '//*[@class="txt-con clear top-padding2"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'cmen.cc'
    source_name = u'国家能源网'
