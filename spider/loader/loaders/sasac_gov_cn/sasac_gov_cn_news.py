# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class SasacGovCnNewsLoader(NewsLoader):

    u"""国务院国有资产监督管理委员会新闻"""

    title_xpath = '//*[@id="con_title"]'
    content_xpath = '//*[@id="con_con"]'

    publish_time_xpath = '//*[@id="con_time"]'
    publish_time_re = u'.*\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@id="con_ly"]'

    source_domain = 'sasac.gov.cn'
    source_name = u'国务院国有资产监督管理委员会'
