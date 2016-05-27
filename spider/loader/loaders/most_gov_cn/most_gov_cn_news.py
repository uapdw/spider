# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class MostGovCnNewsLoader(NewsLoader):

    u"""中华人民共和国科学技术部新闻"""

    title_xpath = '//*[@id="Title"]'
    content_xpath = '//*[@class="trshui13 lh22"]'

    publish_time_xpath = '//*[@class="gray12 lh22"]'
    publish_time_re = u'.*?日期：\s*(\d{4})年(\d{2})月(\d{2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="gray12 lh22"]/script/text()'
    source_re = u'.*str=\s*\'(\S+)\'.*'

    source_domain = 'most.gov.cn'
    source_name = u'中华人民共和国科学技术部'
