# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JxjtcComNewsLoader(NewsLoader):

    u"""江西江钨硬质合金有限公司新闻"""

    title_xpath = '//*[@class="article_show_title"]'
    content_xpath = '//*[@class="article_show_content"]'
    publish_time_xpath = '//*[@class="article_show_info"]'
    publish_time_re = u'.*?发布日期：(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})'
    publish_time_format = '%Y/%m/%d %H:%M:%S'

    source_domain = 'jxjtc.com'
    source_name = u'江西江钨硬质合金有限公司'
