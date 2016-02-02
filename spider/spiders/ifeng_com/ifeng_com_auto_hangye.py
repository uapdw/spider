# -*- coding: utf-8 -*-

from spider.spiders import NewsSpider


class IFengAutoHangyeSpider(NewsSpider):

    u"""凤凰汽车行业爬虫"""

    name = 'ifeng_com_auto_hangye'
    allowed_domains = ['auto.ifeng.com']
    start_urls = ['http://auto.ifeng.com/hangye/']

    target_urls = [
        'auto\.ifeng\.com/hangye/\d{1}.shtml',#文章列表翻页
        'auto\.ifeng\.com/\S+?/\d{8}/\d{1,}.shtml'#文章
    ]

    title_xpath = '//div[@class="arl-cont"]/h3'
    content_xpath = '//div[@class="arl-c-txt"]'
    author_xpath = '//*[@id="author_baidu" or @itemprop="author"]'
    author_re = u'.*?作者：\s*(\S+).*'
    publish_time_xpath = '//*[@id="pubtime_baidu" or @class="ai-date"]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日\s*(\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M'
    source_xpath = '//*[@itemprop="publisher" or @id="source_baidu"]'

    source_domain = 'auto.ifeng.com'
    source_name = u'凤凰汽车'
