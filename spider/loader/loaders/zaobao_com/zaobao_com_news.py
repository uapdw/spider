# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class ZaobaoComNewsLoader(NewsLoader):

    u"""联合早报网新闻"""

    title_xpath = '//*[@id="a_title"]'
    content_xpath = '//*[@id="article_content"]'
    publish_time_xpath = '//*[@class="time"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_domain = 'zaobao.com'
    source_name = u'联合早报网'
