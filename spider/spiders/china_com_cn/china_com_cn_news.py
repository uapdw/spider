# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class ChinaComCnNewsSpider(NewsSpider):

    u"""中国网新闻爬虫"""

    name = 'china_com_cn_news'
    allowed_domains = ['china.com.cn']
    start_urls = ['http://www.china.com.cn/']

    target_urls = [
        'china\.com\.cn/\d{4}-\d{2}/\d{2}/content_\d+\.htm',
        'china\.com\.cn/.*/\d{8}/\d+\.shtml'
    ]

    title_xpath = '//h1'
    content_xpath = '//*[@id="artbody" or @id="fontzoom" or \
                    @class="content" or @class="Content"]'
    author_xpath = '//*[@id="author_baidu"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@id="pubtime_baidu"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="source_baidu"]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'china.com.cn'
    source_name = u'中国网'
