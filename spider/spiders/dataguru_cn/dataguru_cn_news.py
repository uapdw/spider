# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class DataguruNewsSpider(NewsSpider):

    u"""炼数成金新闻爬虫"""

    name = 'dataguru_cn_news'
    allowed_domains = ['dataguru.cn']
    start_urls = ['http://dataguru.cn/']

    target_urls = [
        'dataguru\.cn/article-\d+-\d+\.html'
    ]

    title_xpath = '//*[@class="ph"]'
    content_xpath = '//*[@id="article_content"]'
    author_xpath = '//*[@class="xg1"]'
    author_re = u'.*?原作者:\s*(\S+).*'
    publish_time_xpath = '//*[@class="xg1"]'
    publish_time_re = '.*?(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'
    source_xpath = '//*[@class="xg1"]'
    source_re = u'.*?来自: \s*(\S+).*'

    source_domain = 'dataguru.cn'
    source_name = u'炼数成金'
