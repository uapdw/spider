# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JxipoGovCnNewsLoader(NewsLoader):

    u"""江西省知识产权局新闻"""

    title_xpath = '//*[@class="title"]'
    content_xpath = '//*[@class="neino"]'

    publish_time_xpath = '//*[@class="time"]'
    publish_time_re = u'.*?发布时间：\s*(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})'
    publish_time_format = '%Y/%m/%d %H:%M:%S'

    source_domain = 'jxipo.gov.cn'
    source_name = u'江西省知识产权局'
