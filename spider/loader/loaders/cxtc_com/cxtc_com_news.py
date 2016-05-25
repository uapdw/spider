# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class CxtcComNewsLoader(NewsLoader):

    u"""厦门钨业股份有限公司新闻"""

    title_xpath = '//*[@class="title"]'
    content_xpath = '//*[@class="videonn"]'
    publish_time_xpath = '//*[@class="videonn1"]'
    publish_time_re = u'.*?上传日期：\[(\d{4}-\d{2}-\d{2})\]\s*来源于：\s*\S*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="videonn1"]'
    source_re = u'.*?上传日期：\[\d{4}-\d{2}-\d{2}\]\s*来源于：\s*(\S*)'

    source_domain = 'cxtc.com'
    source_name = u'厦门钨业股份有限公司'
