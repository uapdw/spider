# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class ChinaniaOrgCnNewsLoader(NewsLoader):

    u"""中国有色金属工业协会新闻"""

    title_xpath = '//*[@id="Article"]/h1/text()'
    content_xpath = '//*[@id="Article"]/*[@class="content"]'
    publish_time_xpath = '//*[@id="Article"]/h1/span'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+来源：\S+\s+点击'
    publish_time_format = '%Y-%m-%d %H:%M:%S'
    source_xpath = '//*[@id="Article"]/h1/span'
    source_re = u'.*?\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\s+来源：(\S+)\s+点击'

    source_domain = 'chinania.org.cn'
    source_name = u'中国有色金属工业协会'
