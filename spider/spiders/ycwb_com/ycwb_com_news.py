# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class YCWBNewsSpider(NewsSpider):
    '''金羊网新闻爬虫'''

    name = 'ycwb_com_news'
    allowed_domains = ['ycwb.com']
    start_urls = ['http://www.ycwb.com/']

    target_urls = [
        '\w+\.ycwb.com/\d{4}-\d{2}/\d+/\w+.htm'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@class="main_article"]'
    author_xpath = '//*[@id="author_baidu"]'
    author_re = u'.*?作者：(\S+).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_re = u'.*?发表时间：(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源:(\S+).*'

    source_domain = 'ycwb.com'
    source_name = '金羊网'
