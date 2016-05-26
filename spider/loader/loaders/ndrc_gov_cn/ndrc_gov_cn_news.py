# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class NdrcGovCnNewsLoader(NewsLoader):

    u"""中华人民共和国国家发展和改革委员会新闻"""

    title_xpath = '//*[@class="txt_title1 tleft"]'
    content_xpath = '//*[@class="TRS_Editor"]'
#    author_xpath = ''

    publish_time_xpath = '//*[@class="txt_subtitle1 tleft"]'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2})*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@id="dSourceText"]/a'

    source_domain = 'ndrc.gov.cn'
    source_name = u'中华人民共和国国家发展和改革委员会'
