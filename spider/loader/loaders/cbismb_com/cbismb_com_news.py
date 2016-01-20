# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class CbismbNewsLoader(NewsLoader):

    u"""中小企业IT网新闻爬虫"""

    name = 'cbismb_com_news'
    allowed_domains = ['cbismb.com']
    start_urls = ['http://cbismb.com/']

    target_urls = [
        'cbismb\.com/.*/news/\d{4}-\d{2}-\d{2}/\d+\.html'
    ]

    title_xpath = '//*[@id="cont_title"]'
    content_xpath = '//*[@id="the_content"]'
    author_xpath = '//*[@class="textsource"]'
    author_re = u'.*?作者：\s*(\S+)\s*责任编辑.*'
    publish_time_xpath = '//*[@class="textsource"]'
    publish_time_re = '.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@class="textsource"]'
    source_re = u'.*?来源：\s*(\S+)\s*关键字.*'

    source_domain = 'cbismb.com'
    source_name = u'中小企业IT网'
