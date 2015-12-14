# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class EastDayNewsSpider(NewsSpider):
    '''东方网新闻爬虫'''

    name = 'eastday_com_news'
    allowed_domains = ['eastday.com']
    start_urls = ['http://www.eastday.com/']

    target_urls = [
        '\w+\.eastday.com/\w+/\d{8}/\w+.html'
    ]

    title_xpath = '//*[@id="biaoti"]'
    content_xpath = '//*[@id="zw"]'
    author_xpath = '//*[@class="time grey12a fc lh22"]'
    author_re = u'.*?\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}.*作者:(\S+).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M:%S'
    source_xpath = '//*[@class="time grey12a fc lh22"]'
    source_re = u'.*?\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s*来源:(\S+).*'

    source_domain = 'eastday.com'
    source_name = '东方网'
