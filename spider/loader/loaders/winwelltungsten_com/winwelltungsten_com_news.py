# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class WinwelltungstenComNewsLoader(NewsLoader):

    u"""钨业在线新闻"""

    title_xpath = '//*[@class="article"]/h1'
    content_xpath = '//*[@class="box3"]'
    author_xpath = '//*[@class="box3"]'
    author_re = u'.*?钨业小编：\s*(\S+).*'


    publish_time_xpath = '//*[@class="box1"]'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'

    source_xpath = '//*[@class="box1"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'winwelltungsten.com'
    source_name = u'钨业在线'
