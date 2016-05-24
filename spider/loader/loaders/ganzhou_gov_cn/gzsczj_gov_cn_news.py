# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class GZSCZJNewsLoader(NewsLoader):

    u"""赣州市财政局爬虫"""


    title_xpath = '//*[@id="title"]'
    content_xpath = '//*[@height="323"]'
    #author_xpath = '//*[@id="contentLiability"]'
    #author_re = u'.*?责任编辑:\s*(\S+)\].*'
    publish_time_xpath = '//*[@height="39"]//*[@align="center"]'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{2}-\d{2}).*'
    
    publish_time_format = '%Y-%m-%d'
    #source_xpath = '//*[@class="des"]'
    #source_re = u'.*?来源：\s(\S+?).*'

    source_domain = 'gzsczj.gov.cn'
    source_name = u'赣州市财政局'
