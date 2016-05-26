# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class GovCnNewsLoader(NewsLoader):

    u"""中华人民共和国中央人民政府新闻"""

    title_xpath = '//*[@class="article oneColumn pub_border"]/h1'
    content_xpath = '//*[@class="pages_content"]'

    author_xpath = '//*[@class="editor"]'
    author_re = u'.*?责任编辑：\s*(\S+)'

    publish_time_xpath = '//*[@class="pages-date"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'

    source_xpath = '//*[@class="pages-date"]'
    source_re = u'.*?来源：\s*(\S+)'

    source_domain = 'gov.cn'
    source_name = u'中国人民共和国中央人民政府'
