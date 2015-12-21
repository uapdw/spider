# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class SootooNewsSpider(NewsSpider):

    u"""速途网新闻爬虫"""

    name = 'sootoo_com_news'
    allowed_domains = ['sootoo.com']
    start_urls = ['http://www.sootoo.com/']

    target_urls = [
        'http://www.sootoo.com/content/\d+.shtml'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@id="content"]'
    author_xpath = '//*[@class="t11_info"]'
    author_re = u'.*?作者:\s*(.*)\s*发布.*'
    publish_time_xpath = '//*[@class="t11_info"]'
    publish_time_re = u'.*(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2}:\d{1,2}).*'
    publish_time_format = '%Y%m%d%H:%M'
    source_xpath = '//*[@class="t11_info"]'
    source_re = u'.*?来源:\s*(\S+).*'

    source_domain = 'sootoo.com'
    source_name = u'速途网'
