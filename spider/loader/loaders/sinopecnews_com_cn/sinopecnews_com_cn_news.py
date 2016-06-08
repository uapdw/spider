# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class SinopecnewsComCnNewsLoader(NewsLoader):

    u"""中国石化新闻网新闻"""

    title_xpath = '//*[@id="content"]/table[1]/tr/td/h1/center/b'
    content_xpath = '//*[@class="zw14"]'

    publish_time_xpath = '//*[@id="content"]/table[2]/tr'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@id="content"]/table[2]/tr'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'sinopecnews.com.cn'
    source_name = u'中国石化新闻网'
