# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader, MergeLoader


class JxysOrgCnNewsLoader(NewsLoader):

    u"""江西有色金属信息网新闻"""

    title_xpath = '//*[@id="FontTd"]/../../../table[2]'
    content_xpath = '//*[@id="FontTd"]'
    publish_time_xpath = '//*[@id="FontTd"]/../..//tr[2]'
    publish_time_re = u'.*?发布时间：\[(\d{4}-\d{2}-\d{2})\]'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@id="FontTd"]/../..//tr[2]'
    source_re = u'.*?来源：(\S*)'
    author_xpath = '//*[@id="FontTd"]/../..//tr[2]'
    author_re = u'.*?作者：(\S*)'

    source_domain = 'jxys.org.cn'
    source_name = u'江西有色金属信息网'
