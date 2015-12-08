# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class SapNewsSpider(NewsSpider):

    u"""SAP新闻爬虫"""

    name = 'sap_com_news'
    allowed_domains = ['global.sap.com']
    start_urls = [
        'http://global.sap.com/china/news-reader/index.epx'
    ]

    target_urls = [
        '.*china/news-reader/index\.epx\?.*articleID=\d+.*'
    ]

    title_xpath = '//head/title[1]'
    content_xpath = '//*[@id="articledisplay"]'
    publish_time_xpath = '//*[@class="articledate"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="articlesource"]'

    source_domain = 'sap.com'
    source_name = 'SAP'
