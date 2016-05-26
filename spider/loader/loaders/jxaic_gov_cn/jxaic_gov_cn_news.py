# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JxaicGovCnNewsLoader(NewsLoader):

    u"""江西省工商行政管理局新闻"""

    title_xpath = '//h1'
    content_xpath = '//*[@class="Custom_UnionStyle" or @class="content"]'

    publish_time_xpath = '//*[@class="msgbar"]'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})'
    publish_time_format = '%Y-%m-%d %H:%M:%S'

    source_domain = 'jxaic.gov.cn'
    source_name = u'江西省工商行政管理局'
