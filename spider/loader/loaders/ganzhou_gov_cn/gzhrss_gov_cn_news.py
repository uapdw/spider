# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class GZHrssNewsLoader(NewsLoader):

    u"""贛州市人力资源和社会保障局爬虫"""


    title_xpath = '//*[@class="title"]'
    content_xpath = '//*[@class="content_nr"]'
    #author_xpath = '//*[@id="contentLiability"]'
    #author_re = u'.*?责任编辑:\s*(\S+)\].*'
    publish_time_xpath = '//*[@class="des"]'
    publish_time_re = '.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*'
    
    publish_time_format = '%Y-%m-%d %H:%M'
    #source_xpath = '//*[@class="des"]'
    #source_re = u'.*?来源：\s(\S+?).*'

    source_domain = 'gzhrss.gov.cn'
    source_name = u'贛州市人力资源和社会保障局'
