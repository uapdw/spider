# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class IndaaComCnNewsLoader(NewsLoader):

    u"""英大网新闻"""

    title_xpath = '//*[@class="wyf0221_listbox_top"]/h1'
    content_xpath = '//*[@class="wyf0221_listbox_cont"]'

    author_xpath = '//*[@class="wyf0221_listbox_top"]/dl'
    author_re = u'.*?作者：\s*(\S+).*'

    publish_time_xpath = '//*[@class="wyf0221_listbox_top"]/dl'
    publish_time_re = u'.*?时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="wyf0221_listbox_top"]/dl'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'indaa.com.cn'
    source_name = u'英大网'
