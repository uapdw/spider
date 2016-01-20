# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class LeiphoneNewsLoader(NewsLoader):

    u"""雷锋网新闻爬虫"""

    name = 'leiphone_com_news'
    allowed_domains = ['leiphone.com']
    start_urls = ['http://www.leiphone.com/']

    target_urls = [
        'leiphone\.com/news/\d{6}/\S+\.html'
    ]

    title_xpath = '//*[@class="pageTop"]/h1'
    content_xpath = '//*[contains(@class, "pageCont")]'
    author_xpath = '//*[@class="pi-author"]'
    author_re = u'.*\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}\s*\S+\s*(\S+).*'
    publish_time_xpath = '//*[@class="pi-author"]'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="pi-author"]'
    source_re = u'.*\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}\s*(\S+)\s*\S+.*'

    source_domain = 'leiphone.com'
    source_name = u'雷锋网'
