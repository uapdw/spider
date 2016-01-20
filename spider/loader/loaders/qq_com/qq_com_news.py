# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class QQNewsLoader(NewsLoader):

    u"""腾讯新闻爬虫"""

    name = 'qq_com_news'
    allowed_domains = ['qq.com']
    start_urls = ['http://qq.com']

    target_urls = [
        'news.qq.com/a/\d{8}/\d+.htm'
    ]

    title_xpath = '//*[@class="hd"]/h1'
    content_xpath = '//*[@id="C-Main-Article-QQ"]/*[@class="bd"]'
    author_xpath = '//*[@class="color-a-3"]'
    publish_time_xpath = '//*[@class="article-time"]'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="color-a-1"]/a'
    abstract_xpath = '//meta[@name="Description"]/@content'

    source_domain = 'qq.com'
    source_name = u'腾讯网'
