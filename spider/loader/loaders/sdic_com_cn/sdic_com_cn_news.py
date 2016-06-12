# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class SdicComCnNewsLoader(NewsLoader):

    u"""国家开发投资公司新闻"""

    title_xpath = '//*[@class="title_table_01"]'
    content_xpath = '//*[@id="BodyLabel"]'

    publish_time_xpath = '/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/div[5]'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'sdic.com.cn'
    source_name = u'国家开发投资公司'
