# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class CaijingNewsSpider(NewsSpider):

    u"""财经网新闻爬虫"""

    name = 'caijing_com_cn_news'
    allowed_domains = ['caijing.com.cn']
    start_urls = ['http://www.caijing.com.cn/']

    target_urls = [
        'caijing\.com\.cn/\d{8}/\d+\.shtml'
    ]

    title_xpath = '//*[@id="cont_title"]'
    content_xpath = '//*[@id="the_content"]'
    author_xpath = '//*[@id="editor_baidu"]'
    author_re = u'.*?编辑：\s*(\S+)\).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'

    source_domain = 'caijing.com.cn'
    source_name = u'财经网'
