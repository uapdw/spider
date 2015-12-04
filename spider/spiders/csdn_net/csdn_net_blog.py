# -*- coding: utf-8 -*-

from spider.spiders import BlogSpider


class CSDNBlogSpider(BlogSpider):
    '''CSDN博客爬虫'''

    name = 'csdn_net_blog'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net']

    target_urls = [
        'http://blog.csdn.net/\S+?/article/details/\d+'
    ]

    title_xpath = '//*[@class="link_title"]'
    content_xpath = '//div[@class="article_content"]'
    author_xpath = '//*[@class="user_name"]'
    publish_time_xpath = '//*[@class="link_postdate"]'
    publish_time_format = '%Y-%m-%d %H:%M'

    source_domain = 'csdn.net'
    source_name = 'CSDN'
