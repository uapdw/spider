# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class IFengNewsLoader(NewsLoader):

    u"""凤凰新闻爬虫"""

    name = 'ifeng_com_news'
    allowed_domains = ['ifeng.com']
    start_urls = ['http://www.ifeng.com']

    target_urls = [
        'ifeng\.com/\S+?/\d{8}/\d+_\d{1}.shtml',
        'ifeng\.com/\S+?/\d{4}/\d{4}/\d+.shtml'
    ]

    title_xpath = '//*[@id="artical_topic" or @class="tit01"]'
    content_xpath = '//*[@id="artical_real"]'
    author_xpath = '//*[@id="author_baidu" or @itemprop="author"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@itemprop="datePublished" or @class="time01"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日\s*(\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M'
    source_xpath = '//*[@itemprop="publisher" or @id="source_baidu"]'

    source_domain = 'ifeng.com'
    source_name = u'凤凰网'
