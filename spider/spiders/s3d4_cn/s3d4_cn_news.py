# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class S3d4NewsSpider(NewsSpider):

    u"""说三道四新闻爬虫"""

    name = 's3d4_cn_news'
    allowed_domains = ['s3d4.cn']
    start_urls = ['http://s3d4.cn/']

    target_urls = [
        's3d4\.cn/news/\d+'
    ]

    title_xpath = '//*[@id="left_box"]/h1'
    content_xpath = '//*[@class="articlecontent"]'
    publish_time_xpath = '//*[@class="timebox"]'
    publish_time_re = u'.*发布时间：\s*(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}).*'
    publish_time_format = '%Y/%m/%d %H:%M:%S'
    source_xpath = '//*[@class="timebox"]'
    source_re = u'.*?发布：\s*(\S+).*'

    source_domain = 's3d4.cn'
    source_name = u'说三道四'
