# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class GZSLNewsLoader(NewsLoader):

    u"""赣州市水利局爬虫"""


    title_xpath = '//h2'
    content_xpath = '//*[@class="nnrr"]'
    author_xpath = '//*[@class="data"]'
    author_re = u'.*?作者:\s*(\S+).*'
    publish_time_xpath = '//*[@class="data"]'
    publish_time_re = u'.*?发布时间:\s*(\d{4}-\d{2}-\d{2}).*?'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="data"]'
    source_re = u'.*?文章来源:\s*(\S+).*?作者'

    source_domain = 'gzsl.gov.cn'
    source_name = u'赣州市水利局'
