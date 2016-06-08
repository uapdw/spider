# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class BjxComCnNewsLoader(NewsLoader):

    u"""北极星电力网新闻"""

    title_xpath = '//*[@class="list_detail"]/h1'
    content_xpath = '//*[@id="content"]'

    publish_time_xpath = '//*[@class="list_copy"]'
    publish_time_re = u'.*(\d{4})\/(\d+)\/(\d+).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="list_copy"]/b[1]/a'

    source_domain = 'bjx.com.cn'
    source_name = u'北极星电力网'
