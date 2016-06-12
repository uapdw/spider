# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class SpicComCnNewsLoader(NewsLoader):

    u"""国家电力投资集团公司新闻"""

    title_xpath = '//*[@class="articleTitle"]'
    content_xpath = '//*[@class="TRS_PreAppend"]'

    author_xpath = '//*[@class="articleAttr"]/span[2]'
    author_re = u'.*?作者：\s*(\S+).*'

    publish_time_xpath = '//*[@class="articleAttr"]/span[3]'
    publish_time_re = u'.*?日期：\s*(\d{2}).(\d{2}).(\d{2}).*'
    publish_time_re_join = '-'
    publish_time_format = '%y-%m-%d'

    source_xpath = '//*[@class="articleAttr"]/span[1]'
    source_re = u'.*?来源：\s*(\S+).*'

    source_domain = 'spic.com.cn'
    source_name = u'国家电力投资集团公司'
