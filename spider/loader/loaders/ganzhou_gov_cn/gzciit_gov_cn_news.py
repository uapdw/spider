# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class GZCiitNewsLoader(NewsLoader):

    u"""赣州市工业和信息化委员会爬虫"""


    title_xpath = '//*[@class="lmy-nr"]/h1'
    content_xpath = '//*[@class="lmy-nr-wz"]'
    #author_xpath = '//*[@class="a2"]'
    #author_re = u'.*?发布者:\s*(\S+).*'
    publish_time_xpath = '//*[@class="a1"]'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{2}-\d{2}).*'
    
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="a2"]'
    source_re = u'.*?发布者:\s*(\S+).*'

    source_domain = 'gzciit.gov.cn'
    source_name = u'赣州市工业和信息化委员会'