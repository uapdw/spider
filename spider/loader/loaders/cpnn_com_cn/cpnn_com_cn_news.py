# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class CpnnComCnNewsLoader(NewsLoader):

    u"""中国电力新闻网新闻"""

    title_xpath = '//*[@class="cpnn-con-title"]/h1'
    content_xpath = '//*[@class="cpnn-con-zhenwen"]'

    author_xpath = '//*[@class="cpnn-con-zhenwen"]'
    author_re = u'.*?责任编辑：\s*(\S+).*'

    publish_time_xpath = '//*[@class="cpnn-zhengwen-time"]'
    publish_time_re = u'.*?日期：\s*(\d{2}).(\d{2}).(\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%y-%m-%d'

    source_xpath = '//*[@class="cpnn-zhengwen-time"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'cpnn.com.cn'
    source_name = u'中国电力新闻网'
