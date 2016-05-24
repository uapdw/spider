# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class SinohongdaComNewsLoader(NewsLoader):

    u"""宏达集团新闻"""

    title_xpath = '//*[@class="news_view"]/h3'
    content_xpath = '//*[@id="news_ext_content"]'
    publish_time_xpath = '//*[@class="news_view"]/h2'
    publish_time_re = u'.*?发布时间：(\d{4})年(\d{2})月(\d{2})日'
    publish_time_re_join = u'-'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'sinohongda.com'
    source_name = u'宏达集团'
