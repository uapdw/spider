# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JxdoftecGovCnNewsLoader(NewsLoader):

    u"""江西省商务厅新闻"""

    title_xpath = '//*[@id="newstitl"]'
    content_xpath = '//*[@id="xx"]'

    publish_time_xpath = '//*[@id="newsdate"]'
    publish_time_re = u'.*?日期：\[(\d{4}-\d{1,2}-\d{1,2})\]'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@id="newsdate"]'
    source_re = u'.*?来源：\[\s*(\S*?)\s*\]'

    source_domain = 'jxdoftec.gov.cn'
    source_name = u'江西省商务厅'
