# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class CctimeNewsSpider(NewsSpider):
    '''飞象网新闻爬虫'''

    name = 'cctime_com_news'
    allowed_domains = ['cctime.com']
    start_urls = ['http://www.cctime.com/']

    target_urls = [
        'cctime\.com/html/\d{4}-\d{1,2}-\d{1,2}/\d+\.htm'
    ]

    title_xpath = '//title'
    content_xpath = '//*[@class="art_content"]'
    author_xpath = '//*[@class="editor"]'
    author_re = u'.*?编\s*辑：\s*(\S+).*'
    publish_time_xpath = '//*[@class="dateAndSource"]'
    publish_time_re = u'.*(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2}:\d{1,2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d-%H:%M'
    source_xpath = '//*[@class="dateAndSource"]'
    source_re = u'.*\d{4}年\d{1,2}月\d{1,2}日\s*\d{1,2}:\d{1,2}\s*(\S+).*'

    source_domain = 'cctime.com'
    source_name = u'飞象网'
