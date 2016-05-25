# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class GZSdpcNewsLoader(NewsLoader):

    u"""赣州市发展和改革委员会爬虫"""


    title_xpath = '//*[@class="tdtitle"]'
    content_xpath = '//*[@id="artibody"]'
    #author_xpath = '//*[@class="a2"]'
    #author_re = u'.*?发布者:\s*(\S+).*'
    publish_time_xpath = '//*[@height="30"]'
    publish_time_re = u'.*?日期：\s*(\d{4})年(\d+)月(\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@height="30"]/script/text()'
    source_re = '.*?l="(\S+)"'

    source_domain = 'gzsdpc.gov.cn'
    source_name = u'赣州市发展和改革委员会'