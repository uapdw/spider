# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class GhkjComNewsLoader(NewsLoader):

    u"""北京国华科技集团有限公司新闻"""

    title_xpath = '//*[@class="STYLE3"]/table[1]/tr[1]/td/span'
    content_xpath = '//*[@class="STYLE3"]/table[2]/tr/td'

    publish_time_xpath = '//*[@class="STYLE3"]/table[1]/tr[3]/td[4]'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'ghkj.com'
    source_name = u'北京国华科技集团有限公司'
