# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class NewsSmmCnNewsLoader(NewsLoader):

    u"""上海有色网新闻"""

    title_xpath = '//*[@class="news-title"]/h1'
    content_xpath = '//*[@class="news-detail"]'
    publish_time_xpath = '//*[@class="news-title"]/div[@class="note"]'
    publish_time_re = u'.*?(\d{4}-\d{2}-\d{2})\s*来源:\s*\S*'
    publish_time_format = '%Y-%m-%d'
    source_xpath = '//*[@class="news-title"]/div[@class="note"]'
    source_re = u'.*?\d{4}-\d{2}-\d{2}\s*来源:\s*(\S*)'

    source_domain = 'news.smm.cn'
    source_name = u'上海有色网'
