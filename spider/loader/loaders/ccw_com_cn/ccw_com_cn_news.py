# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class CcwNewsLoader(NewsLoader):

    u"""计世网新闻爬虫"""

    name = 'ccw_com_cn_news'
    allowed_domains = ['ccw.com.cn']
    start_urls = ['http://www.ccw.com.cn/']

    target_urls = [
        'http://www.ccw.com.cn/article/view/\d+'
    ]

    title_xpath = '//div[@class="hd"]/h1'
    content_xpath = '//*[@class="bd"]'
    author_xpath = '//*[@class="author"]'
    author_re = u'.*?(.*)-.*'
    publish_time_xpath = '//*[@class="author"]'
    publish_time_re = u'.*(\d{4}).(\d{2}).(\d{2})\s+(\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M'

    source_domain = 'ccw.com.cn'
    source_name = u'计世网'
