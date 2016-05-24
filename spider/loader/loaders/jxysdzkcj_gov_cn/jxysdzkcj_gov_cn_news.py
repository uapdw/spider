# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JxysdzkcjGovCnNewsLoader(NewsLoader):

    u"""江西有色地质勘查局新闻"""

    title_xpath = '//*[@class="MsoNormal"]'
    content_xpath = '//*[@id="infoContent"]'
    publish_time_xpath = '//*[@class="date"]'
    publish_time_re = u'.*?日期：\s*(\d{4})年(\d{1,2})月(\d{1,2})日\s+(\d{2}:\d{2})'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d-%H:%M'

    source_domain = 'jxysdzkcj.gov.cn'
    source_name = u'江西有色地质勘查局'
