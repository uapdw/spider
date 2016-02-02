# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class AutohomeNewsLoader(NewsLoader):
    u"""汽车之家新闻爬虫"""

    title_xpath = '//*[@class="area article"]/h1'
    content_xpath = '//*[@class="article-content"]'
    author_xpath = '//*[@class="article-info"]/span[4]'
    author_re = u'.*?编辑：\s*(\S+).*'
    publish_time_xpath = '//*[@class="article-info"]/span[1]'
    publish_time_re = u'.*?(\d{4})年(\d{2})月(\d{2})日\s+(\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M'
    source_xpath = '//*[@class="article-info"]/span[2]'
    source_re = u'.*?来源：\s*(\S+).*'

    site_domain = 'autohome.com.cn'
    site_name = u'汽车之家'
