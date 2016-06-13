# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class ChngComCnNewsLoader(NewsLoader):

    u"""中国华能集团公司新闻"""

    title_xpath = '/html/body/table[2]/tr/td/table[2]/tr[2]'
    content_xpath = '//*[@id="Zoom2"]'

    author_xpath = '/html/body/table[2]/tr/td/table[2]/tr[4]/td/table/tr/td'
    author_re = u'.*?作者:\s*(\S+).*'

    publish_time_xpath = '/html/body/table[2]/tr/td/table[2]/tr[4]/td/table/tr/td'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '/html/body/table[2]/tr/td/table[2]/tr[4]/td/table/tr/td'
    source_re = u'.*?信息来源:\s*(\S+).*'

    source_domain = 'chng.com.cn'
    source_name = u'中国华能集团公司'
