# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class CnitdcComNewsLoader(NewsLoader):

    u"""中国矿冶设备供求网新闻"""

    title_xpath = '//h1'
    content_xpath = '//*[@class="content"]'
    publish_time_xpath = '//*[@id="info"]'
    publish_time_re = u'.*?时间:(\d{4}/\d{1,2}/\d{1,2})\s+来源:\S+\s+编辑:\s+\S+'
    publish_time_format = '%Y/%m/%d'
    source_xpath = '//*[@id="info"]'
    source_re = u'.*?时间:\d{4}/\d{1,2}/\d{1,2}\s+来源:(\S+)\s+编辑:\s+\S+'

    source_domain = 'cnitdc.com'
    source_name = u'中国有色金属科技信息网'
