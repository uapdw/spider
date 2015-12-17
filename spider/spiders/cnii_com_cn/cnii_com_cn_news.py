# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class CniiComCnNewsSpider(NewsSpider):

    u"""中国信息产业网新闻爬虫"""

    name = 'cnii_com_cn_news'
    allowed_domains = ['cnii.com.cn']
    start_urls = ['http://www.cnii.com.cn/']

    target_urls = [
        'http://www.cnii.com.cn/\w+/\d{4}-\d{2}/\d+/\w+.htm'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@class="conzw"]'
    author_xpath = '//*[@class="conzz"]'
    author_re = u'.*?作者：(.*).*'
    publish_time_xpath = '//*[@class="conzz"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="conzz"]'
    source_re = u'.*?来源：(\S+).*'

    source_domain = 'cnii.com.cn'
    source_name = u'中国信息产业网'
