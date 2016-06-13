# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class DqzyxyNetNewsLoader(NewsLoader):

    u"""大庆职业学院新闻"""

    title_xpath = '//*[@class="c_title_text"]/h2'
    content_xpath = '//*[@class="c_content_overflow"]'

    author_xpath = '//*[@class="c_title_author"]/span[1]'
    author_re = u'.*?作者：\s*(\S+).*'

    publish_time_xpath = '//*[@class="c_title_author"]/span[3]'
    publish_time_re = u'.*?发布日期：\s*(\d{4})年(\d{2})月(\d{2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="c_title_author"]/span[2]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'dqzyxy.net'
    source_name = u'大庆职业学院'
