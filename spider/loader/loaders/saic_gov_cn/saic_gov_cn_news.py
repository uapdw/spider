# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class SaicGovCnNewsLoader(NewsLoader):

    u"""中华人民共和国国家工商行政管理总局新闻"""

    title_xpath = '//*[@class="blue_dzi"]'
    content_xpath = '//*[@class="TRS_Editor"]'

    publish_time_xpath = '//*[@class="zj_four_time"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="zj_four_time"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'saic.gov.cn'
    source_name = u'中华人民共和国国家工商行政管理总局'
