# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JiangXiNewsLoader(NewsLoader):

    u"""江西省人民政府爬虫"""


    title_xpath = '//*[@class="columnXLBT"]'
    content_xpath = '//*[@class="artibody"]'
    #author_xpath = '//*[@class="zhweL"]/script/text()'
    #author_re = '.*?source=\s*\'\S+\s*(\S+)\';'
    publish_time_xpath = '//*[@class="columnXLBM"]'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{2}-\d{2}).*'
    
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="zhweL"]/script/text()'
    source_re = '.*?source=\s*\'(\S+)\'.*'

    source_domain = 'jiangxi.gov.cn'
    source_name = u'江西省人民政府'