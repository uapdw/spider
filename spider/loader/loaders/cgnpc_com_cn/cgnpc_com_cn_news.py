# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class CgnpcComCnNewsLoader(NewsLoader):

    u"""中广核新闻"""

    title_xpath = '//*[@class="col-xs-9 newscontent"]/h4'
    content_xpath = '//*[@class="contact-text"]'

    publish_time_xpath = '//*[@class="info"]/span[1]'
    publish_time_re = u'.*?发稿时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'cgnpc.com.cn'
    source_name = u'中广核'
