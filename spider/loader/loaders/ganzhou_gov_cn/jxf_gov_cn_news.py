# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JXFNewsLoader(NewsLoader):

    u"""江西省财政厅爬虫"""


    title_xpath = '//*[@class="showtitle"]'
    content_xpath = '//*[@class="showcontent"]'

    publish_time_xpath = '//*[@height="24"]'
    publish_time_re = u'.*?更新日期：\s*(\d{4}-\d{1,2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@height="24"]'
    source_re = u'.*?信息来源：\s*(\S+).*'

    source_domain = 'jxf.gov.cn'
    source_name = u'江西省财政厅'