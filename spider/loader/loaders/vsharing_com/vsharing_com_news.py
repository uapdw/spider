# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class VsharingNewsLoader(NewsLoader):

    u"""畅享网新闻爬虫"""

    name = 'vsharing_com_news'
    allowed_domains = ['vsharing.com']
    start_urls = ['http://www.vsharing.com/']

    target_urls = [
        'http://www.vsharing.com/\w+/\w+/\d{4}-\d+/\d+.html'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@class="content_art"]'
    author_xpath = '//div[@class="summary_author"]/div/div'
    author_re = u'.*?作者：\s*\S+\s+(.*).*'
    publish_time_xpath = '//*[@class="summary_author"]'
    publish_time_re = u'.*(\d{4})/(\d{2})/(\d{2})\s+(\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M:%S'
    source_xpath = '//div[@class="summary_author"]/div/div/span'
#     source_re = u'.*?来源：(\S+).*'

    source_domain = 'vsharing.com'
    source_name = u'畅享网'
