# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class QianLongNewsSpider(NewsSpider):
    '''千龙网新闻爬虫'''

    name = 'qianlong_com_news'
    allowed_domains = ['qianlong.com']
    start_urls = ['http://www.qianlong.com/']

    target_urls = [
        '\w+\.qianlong.com/\d{4}/\d{4}/\d{6}\.shtml'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@class="article-content"]'
    author_xpath = '//*[@class="editor"]/span'
    publish_time_xpath = '//*[@class="pubDate"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d%H:%M'
    source_xpath = '//*[@class="source"]'

    source_domain = 'qianlong.com'
    source_name = '千龙网'
