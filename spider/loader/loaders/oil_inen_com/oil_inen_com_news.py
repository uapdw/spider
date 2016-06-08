# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class OilInenComNewsLoader(NewsLoader):

    u"""国际石油网新闻"""

    title_xpath = '//*[@class="c_content"]/h1'
    content_xpath = '//*[@id="content"]'

    publish_time_xpath = '//*[@class="c_copy"]'
    publish_time_re = u'.*?日期：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="c_copy"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'oil.in-en.com'
    source_name = u'国际石油网'
