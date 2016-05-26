# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JXDpcNewsLoader(NewsLoader):

    u"""江西省发改委爬虫"""


    title_xpath = '//*[@class="tdtitle"]'
    content_xpath = '//*[@class="cas_content"]'
    author_xpath = '//*[@height="60"]/div/script/text()'
    author_re = '.*?l=\s*"(\S+)".*'
    publish_time_xpath = '//*[@height="60"]/div'
    publish_time_re = u'.*?日期：\s*(\d{4})年(\d{1,2})月(\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@height="60"]/div/script/text()'
    source_re = '.*?s=\s*"(\S+)".*'

    source_domain = 'jxdpc.gov.cn'
    source_name = u'江西省发改委'