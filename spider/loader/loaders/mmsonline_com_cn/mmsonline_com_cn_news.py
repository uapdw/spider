# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class MmsonlineComCnNewsLoader(NewsLoader):

    u"""国际金属加工网新闻"""

    title_xpath = '//*[@class="news_caption"]/h1'
    content_xpath = '//*[@class="news_content"]'
    publish_time_xpath = '//*[@class="news_date"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="news_date"]'
    source_re = u'.*?(\S+)\s*\d{4}年\d{2}月\d{2}日.*'

    source_domain = 'mmsonline.com.cn'
    source_name = u'国际金属加工网'
