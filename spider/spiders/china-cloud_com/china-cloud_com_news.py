# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class ChinaCloudNewsSpider(NewsSpider):

    u"""中云网新闻爬虫"""

    name = 'china-cloud_com_news'
    allowed_domains = ['china-cloud.com']
    start_urls = ['http://www.china-cloud.com/']

    target_urls = [
        'china-cloud\.com/.*/\d{8}_\d+\.html'
    ]

    title_xpath = '//*[@class="wenzhang_top"]/h2'
    content_xpath = '//*[@class="zhengwen"]'
    author_xpath = '//*[@class="sm_arcinfo"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@class="sm_arcinfo"]'
    publish_time_re = u'.*时间：\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="sm_arcinfo"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'china-cloud.com'
    source_name = u'中云网'
