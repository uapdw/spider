# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class YzpcComCnNewsLoader(NewsLoader):

    u"""长江石化新闻"""

    title_xpath = '//*[@class="box pd5"]/h1'
    content_xpath = '//*[@class="box pd5"]/div[2]'

    publish_time_xpath = '//*[@class="date"]'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'yzpc.com.cn'
    source_name = u'长江石化'
