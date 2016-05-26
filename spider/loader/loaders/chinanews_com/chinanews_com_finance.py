# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class ChinanewsFinanceLoader(NewsLoader):

    u"""中新网财经爬虫"""

    title_xpath = '//*[@id="newstitle"]/@value'
    content_xpath = '//*[@class="left_zw"]'
    author_xpath = '//*[@id="editorname"]/@value'
    publish_time_xpath = '//*[@class="left-t"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日\s+(\d+:\d+).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d-%H:%M'

    source_xpath = '//*[@class="left-t"]'
    source_re = u'.*?\d{4}年\d{2}月\d{2}日\s+\d+:\d+.*?来源：\s*(\S+)'

    source_domain = 'chinanews.com'
    source_name = u'中新网'
