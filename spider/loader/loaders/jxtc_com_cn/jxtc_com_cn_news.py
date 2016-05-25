# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JxtcComCnNewsLoader(NewsLoader):

    u"""江钨集团新闻"""

    title_xpath = '//*[@class="title taC"]'
    content_xpath = '//*[@class="tcontext"]'
    publish_time_xpath = '//*[@class="pF12 taC"]'
    publish_time_re = u'.*?发布时间：(\d{4}-\d{2}-\d{2})\s+来源：\S*\s*作者：.*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="pF12 taC"]'
    source_re = u'.*?发布时间：\d{4}-\d{2}-\d{2}\s+来源：(\S*)\s*作者：.*'
    author_xpath = '//*[@class="pF12 taC"]'
    author_re = u'.*?发布时间：\d{4}-\d{2}-\d{2}\s+来源：\S*\s*作者：(.*)'

    source_domain = 'jxtc.com.cn'
    source_name = u'江钨集团'
