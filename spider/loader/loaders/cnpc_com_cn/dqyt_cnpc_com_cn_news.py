# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class DqytCnpcComCnNewsLoader(NewsLoader):

    u"""中国石油大庆油田新闻"""

    title_xpath = '//*[@class="content_title"]'
    content_xpath = '//*[@class="ms-rtestate-field"]'

    author_xpath = '//*[@id="contentText"]/span[3]'
    author_re = u'.*?责任编辑：\s*(\S+).*'

    publish_time_xpath = '//*[@id="contentText"]/span[1]'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@id="contentText"]/span[2]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'dqyt.cnpc.com.cn'
    source_name = u'中国石油大庆油田'
