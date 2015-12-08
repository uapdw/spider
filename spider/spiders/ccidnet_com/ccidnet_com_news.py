# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class CcidnetNewsSpider(NewsSpider):
    '''赛迪网新闻爬虫'''

    name = 'ccidnet_com_news'
    allowed_domains = ['ccidnet.com']
    start_urls = ['http://www.ccidnet.com/']

    target_urls = [
        'ccidnet\.com/\d{4}/\d{4}/\d+\.shtml'
    ]

    title_xpath = '//h2'
    content_xpath = '//*[@class="main_content"]'
    author_xpath = '//*[@class="tittle_j"]'
    author_re = u'.*?（作者：\S+?）.*'
    publish_time_xpath = '//*[@class="tittle_j"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="tittle_j"]'
    source_re = u'.*?（来源：\S+?）.*'

    source_domain = 'ccidnet.com'
    source_name = u'赛迪网'
