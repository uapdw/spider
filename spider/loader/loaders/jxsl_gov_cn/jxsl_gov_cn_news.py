# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JxslGovCnNewsLoader(NewsLoader):

    u"""江西省水利厅新闻"""

    title_xpath = '//*[@class="wzycenter1"]/text()'
    content_xpath = '//*[@class="wzycenter2"]'

    publish_time_xpath = '//*[@class="wzycenter3"]'
    publish_time_re = u'.*?发布时间：(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})'
    publish_time_format = '%Y-%m-%d %H:%M:%S'

    source_domain = 'jxsl.gov.cn'
    source_name = u'江西省水利厅'
