# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class GZ315NewsLoader(NewsLoader):

    u"""赣州市工商行政管理局爬虫"""


    title_xpath = '//h1'
    content_xpath = '//*[@class="c_r"]'
    author_xpath = '//*[@class="c_bar"]'
    author_re = u'.*?发布人：\s*(\S+).*?浏览'
    publish_time_xpath = '//*[@class="c_bar"]'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="c_bar"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'gz315.gov.cn'
    source_name = u'赣州市工商行政管理局'