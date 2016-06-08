# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class SinopecgroupComNewsLoader(NewsLoader):

    u"""中国石化新闻"""

    title_xpath = '//*[@class="lfnews-title"]'
    content_xpath = '//*[@class="lfnews-content"]'

    publish_time_xpath = '//*[@class="lfnews-bottom-right"]'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="lfnews-bottom-left"]'
    source_re = u'.*?信息来源：\s*(\S+).*'

    source_domain = 'sinopecgroup.com'
    source_name = u'中国石化'
