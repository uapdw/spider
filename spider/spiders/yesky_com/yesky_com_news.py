# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class YeskyComNewsSpider(NewsSpider):

    u"""天极网新闻爬虫"""

    name = 'yesky_com_news'
    allowed_domains = ['yesky.com']
    start_urls = ['http://www.yesky.com/']

    target_urls = [
        'yesky.com/\d+/\d+.shtml'
    ]

    title_xpath = '//*[@class="title"]'
    content_xpath = '//*[@class="article"]'
    author_xpath = '//*[@class="editor"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="detail"]/span[2]'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="detail"]/span[1]'

    source_domain = 'yesky.com'
    source_name = u'天极网'
