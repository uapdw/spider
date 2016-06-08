# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class China5eComNewsLoader(NewsLoader):

    u"""中国能源网新闻"""

    title_xpath = '//*[@class="showtitle"]/h1'
    content_xpath = '//*[@class="showcontent"]'
    
    publish_time_xpath = '//*[@class="showtitinfo"]'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'

    source_xpath = '//*[@class="showtitinfo"]'
    source_re = u'.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (\S+)\s*作者：\s*\S+.*'

    source_domain = 'china5e.com'
    source_name = u'中国能源网'
