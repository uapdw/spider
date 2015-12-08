# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class N199itNewsSpider(NewsSpider):
    '''199it新闻爬虫'''

    name = '199it_com_news'
    allowed_domains = ['199it.com']
    start_urls = ['http://www.199it.com/']

    target_urls = [
        '199it\.com/archives/\d+\.html'
    ]

    title_xpath = '//*[@class="entry-title"]'
    content_xpath = '//*[@class="entry-content"]'
    publish_time_xpath = '//*[@class="search-post-info-table"]'
    publish_time_re = u'.*(\d{4})年(\d{2})月(\d{1,2})日.*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'

    source_domain = '199it.com'
    source_name = '199it'
