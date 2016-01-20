# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class EworksNewsLoader(NewsLoader):

    u"""e-works新闻爬虫"""

    name = 'eworks_net_cn_news'
    allowed_domains = ['e-works.net.cn']
    start_urls = ['http://www.e-works.net.cn/']

    target_urls = [
        'http://\w+.e-works.net.cn/\w+/\w+.htm'
    ]

    title_xpath = '//h1'
    content_xpath = '//div[@class="mt15 f14 lh240 WaresDetail"]'
    author_xpath = '//div[@class="fl mt10"]'
    author_re = u'.*?作者：(.*)关键字：.*'
    publish_time_xpath = '//div[@class="fl mt10" or @class="fl mt10 pb10"]'
    publish_time_re = u'.*(\d{4})[年|/](\d{1,2})[月|/](\d{1,2}).*'
    publish_time_format = '%Y%m%d'
    source_xpath = '//div[@class="fl mt10"]'
    source_re = u'.*?来源：(\S+).*'

    source_domain = 'e-works.net.cn'
    source_name = u'e-works'
