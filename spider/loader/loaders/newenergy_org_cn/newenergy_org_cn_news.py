# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class NewenergyOrgCnNewsLoader(NewsLoader):

    u"""中国新能源网新闻"""

    title_xpath = '//*[@class="articlebox"]/tr/td/h2'
    content_xpath = '//*[@class="bodybox"]'

    author_xpath = '//*[@class="infor"]'
    author_re = u'.*?作者：\s*(\S+).*'

    publish_time_xpath = '//*[@class="infor"]'
    publish_time_re = u'.*?发布日期：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="infor"]'
    source_re = u'.*?文章来源：\s*(\S+).*'

    source_domain = 'newenergy.org.cn'
    source_name = u'中国新能源网'
