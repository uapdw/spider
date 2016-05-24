# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class GZDoFComNewsLoader(NewsLoader):

    u"""赣州市商务局爬虫"""


    title_xpath = '//h4'
    content_xpath = '//*[@class="cont"]'
    #author_xpath = '//*[@id="contentLiability"]'
    #author_re = u'.*?责任编辑:\s*(\S+)\].*'
    publish_time_xpath = '//h3'
    publish_time_re = u'.*?发布时间:\s*(\d+)年(\d+)月(\d+).*?'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//h3'
    source_re = u'.*?文章来源 :\s*(\S+).*'

    source_domain = 'gzdofcom.gov.cn'
    source_name = u'赣州市商务局'
