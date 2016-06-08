# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class SuCnNewsLoader(NewsLoader):

    u"""石油网新闻"""

    title_xpath = '//*[@class="title"]/h1'
    content_xpath = '//*[@class="content"]'

    publish_time_xpath = '//*[@class="title"]/h6'
    publish_time_re = u'.*?时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="title"]/h6'
    source_re = u'.*信息来源：\s*(\S+).*'

    source_domain = 's-u.cn'
    source_name = u'石油网'
