# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class XinhuanetNewsLoader(NewsLoader):

    u"""新华网新闻爬虫"""

    name = 'xinhuanet_com_news'
    allowed_domains = ['xinhuanet.com']
    start_urls = ['http://xinhuanet.com/']

    target_urls = [
        'news\.xinhuanet\.com/\S+/\d{4}-\d{2}/\d{2}/c_\d+.htm'
    ]

    title_xpath = '//*[@id="title"]'
    content_xpath = '//*[@class="article" or @class="news_con" or \
                     @id="content"]'
    author_xpath = '//*[@class="editor" or @id="editblock"]'
    author_re = u'.*?编辑: \s*(\S+).*'
    publish_time_xpath = '//*[@class="time" or @id="pubtimeandfrom" or \
                          @id="pubtime"]'
    publish_time_re = u'.*?(\d{4})[年|-](\d{2})[月|-](\d{2}).*?\
                        (\d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M:%S'
    source_xpath = '//*[@class="source" or @id="from" or @id="source"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'xinhuanet.com'
    source_name = u'新华网'
