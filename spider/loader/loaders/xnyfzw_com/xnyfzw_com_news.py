# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class XnyfzwComNewsLoader(NewsLoader):

    u"""新能源发展网新闻"""

    title_xpath = '//*[@class="newstitle"]'
    content_xpath = '//*[@class="content"]'

    publish_time_xpath = '//*[@class="info"]'
    publish_time_re = u'.*?发布日期：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="info"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'xnyfzw.com'
    source_name = u'新能源发展网'
