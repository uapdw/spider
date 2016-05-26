# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JXHrssNewsLoader(NewsLoader):

    u"""江西省人力资源和社会保障厅爬虫"""


    title_xpath = '//*[@id="caption"]'
    content_xpath = '//*[@class="content"]'

    publish_time_xpath = '//*[@id="authortime"]'
    publish_time_re = u'.*?发表时间：\s*\[\s*(\d{4}-\d{1,2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@id="authortime"]'
    source_re = u'.*?来源：\s*\[\s*(\S+)\s*\]'

    source_domain = 'jxhrss.gov.cn'
    source_name = u'江西省人力资源和社会保障厅'