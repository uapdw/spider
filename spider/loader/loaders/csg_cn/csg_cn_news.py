# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class CsgCnNewsLoader(NewsLoader):

    u"""中国南方电网新闻"""

    title_xpath = '//*[@id="articleTitle"]/h2'
    content_xpath = '//*[@class="TRS_Editor"]'

    publish_time_xpath = '//*[@id="articleTitle"]/h4'
    publish_time_re = u'.*?发布时间\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@id="articleTitle"]/h4'
    source_re = u'.*?信息来源：\s*(\S+).*'

    source_domain = 'csg.cn'
    source_name = u'中国南方电网'
