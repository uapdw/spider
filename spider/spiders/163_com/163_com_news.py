# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class WWW163NewsSpider(NewsSpider):
    '''网易新闻爬虫'''

    name = '163_com_news'
    allowed_domains = ['163.com']
    start_urls = ['http://www.163.com/']

    target_urls = [
        '\S+\.163.com/\d{2}/\d{4}/\d+/\S+.html'
    ]

    title_xpath = '//h1[@id="h1title"]'
    content_xpath = '//div[@class="end-text"]'
    author_xpath = '//*[contains(@class, "ep-source")]/*[@class="left"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[contains(@class, "ep-time-soure")]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[contains(@class, "ep-source")]/*[@class="left"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = '163.com'
    source_name = '网易'
