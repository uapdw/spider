# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class CsuEduCnNewsLoader(NewsLoader):

    u"""中南大学新闻"""

    title_xpath = '//*[@class="subTitle2"]'
    content_xpath = '//div[@class="subCont"]'
    publish_time_xpath = '//*[@class="otherTme"]'
    publish_time_re = u'.*?来源：\S+.*?发布时间：(\d{4})年(\d{2})月(\d{2})日\s*作者：\s*\S*'
    publish_time_re_join = '-'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="otherTme"]'
    source_re = u'.*?来源：(\S+).*?发布时间：\d{4}年\d{2}月\d{2}日\s*作者：\s*\S*'
    author_xpath = '//*[@class="otherTme"]'
    author_re = u'.*?来源：\S+.*?发布时间：\d{4}年\d{2}月\d{2}日\s*作者：\s*(\S*)'

    source_domain = 'csu.edu.cn'
    source_name = u'中南大学'
