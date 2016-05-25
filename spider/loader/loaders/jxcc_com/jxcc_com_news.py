# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class JxccComNewsLoader(NewsLoader):

    u"""江铜集团新闻"""

    title_xpath = '//*[@class="news_text_title"]'
    content_xpath = '//*[@id="info_content"]'
    publish_time_xpath = '//*[@class="news_text_other"]'
    publish_time_re = u'.*?发布时间:(\d{4}-\d{2}-\d{2})\s+浏览量：\d+\s+来源：\s*\S*\s*作者：\s*\S*\s*【'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="news_text_other"]'
    source_re = u'.*?发布时间:\d{4}-\d{2}-\d{2}\s+浏览量：\d+\s+来源：\s*(\S*)\s*作者：\s*\S*\s*【'
    author_xpath = '//*[@class="news_text_other"]'
    author_re = u'.*?发布时间:\d{4}-\d{2}-\d{2}\s+浏览量：\d+\s+来源：\s*\S*\s*作者：\s*(\S*)\s*【'

    source_domain = 'jxcc.com'
    source_name = u'江铜集团'
