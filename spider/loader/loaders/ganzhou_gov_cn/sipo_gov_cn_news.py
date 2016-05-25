# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class SiPoNewsLoader(NewsLoader):

    u"""全国知识产权局系统政府门户网站-江西子站爬虫"""


    title_xpath = '//*[@class="index_title"]'
    content_xpath = '//*[@id="printContent"]'
    #author_xpath = '//*[@class="c_bar"]'
    #author_re = u'.*?发布人：\s*(\S+).*?浏览'
    publish_time_xpath = '//*[@class="index_time"]'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    #source_xpath = '//*[@class="c_bar"]'
    #source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'sipo.gov.cn'
    source_name = u'全国知识产权局系统政府门户网站-江西子站'