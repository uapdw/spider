# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class CsrcGovCnNewsLoader(NewsLoader):

    u"""中国证券监督管理委员会新闻"""

    title_xpath = '//*[@class="title"]'
    content_xpath = '//*[@class="Custom_UnionStyle"]'

    publish_time_xpath = '//*[@class="time"]'
    publish_time_re = u'.*?时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="time"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'csrc.gov.cn'
    source_name = u'中国证券监督管理委员会'
