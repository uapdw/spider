# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class MlrGovCnNewsLoader(NewsLoader):

    u"""中华人民共和国国土资源部新闻"""

    title_xpath = '//*[@class="zw_title"]'
    content_xpath = '//*[@id="content1"]'

    author_xpath = '//*[@class="Gray12"]'
    author_re = u'.*?作者：\s*(\S+).*'

    publish_time_xpath = '//*[@class="Gray12"]'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="Gray12"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'mlr.gov.cn'
    source_name = u'中华人民共和国国土资源部'
