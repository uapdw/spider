# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class CnoocComCnNewsLoader(NewsLoader):

    u"""中国海油新闻"""

    title_xpath = '//*[@id="article"]/tr[1]/td'
    content_xpath = '//*[@id="article"]/tr[4]/td/table[2]'

    publish_time_xpath = '//*[@id="article"]/tr[3]/td/table/tr/td[1]'
    publish_time_re = u'.*?发布日期：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@id="article"]/tr[3]/td/table/tr/td[3]'
    source_re = u'.*?信息来源：\s*(\S+).*'

    source_domain = 'cnooc.com.cn'
    source_name = u'中国海油'
