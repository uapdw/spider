# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class GanZhouNewsLoader(NewsLoader):

    u"""贛州人民政府爬虫"""


    title_xpath = '//*[@class="contentborder"]//*[@class="tdtitle"]'
    content_xpath = '//*[@class="contentborder"]//*[@id="artibody"]'
    #author_xpath = '//*[@id="contentLiability"]'
    #author_re = u'.*?责任编辑:\s*(\S+)\].*'
    publish_time_xpath = '//*[@class="contentborder"]//*[@class="style02"]'
    publish_time_re = u'.*?(\d+)年(\d+)月(\d+).*?'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="contentborder"]//*[@class="style02"]/script/text()'
    source_re = '.*?l="(\S+)"'

    source_domain = 'ganzhou.gov.cn'
    source_name = u'贛州市人民政府'
