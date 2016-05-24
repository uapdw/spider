# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader, MergeLoader


class CtiaComCnNewsLoader(MergeLoader):
    def __init__(self):
        super(CtiaComCnNewsLoader, self).__init__([
            CtiaComCnNewsLoader1(), CtiaComCnNewsLoader2()
        ])


class CtiaComCnNewsLoader1(NewsLoader):

    u"""中国钨业协会新闻"""

    title_xpath = '//*[@id="fontzoom"]/h1'
    content_xpath = '//*[@id="fontzoom"]'
    publish_time_xpath = '//*[@class="left_tdbgall"]'
    publish_time_re = u'.*?更新时间：\s*(\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2})'
    publish_time_format = '%Y-%m-%d %H:%M:%S'

    source_domain = 'ctia.com.cn'
    source_name = u'中国钨业协会'


class CtiaComCnNewsLoader2(NewsLoader):

    u"""中国钨业协会新闻"""

    title_xpath = '//*[@id="fontzoom"]/strong'
    content_xpath = '//*[@id="fontzoom"]'
    publish_time_xpath = '//*[@class="left_tdbgall"]'
    publish_time_re = u'.*?更新时间：\s*(\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2})'
    publish_time_format = '%Y-%m-%d %H:%M:%S'

    source_domain = 'ctia.com.cn'
    source_name = u'中国钨业协会'
