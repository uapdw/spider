# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader


class XcarComCnNewsLoader(NewsLoader):
    u"""爱卡汽车新闻爬虫"""

    title_xpath = '//*[@class="article_title"]/h1'
    content_xpath = '//*[@class="artical_player_wrap"]'
    author_xpath = '//*[@class="media_user"]'
    publish_time_xpath = '//*[@class="pub_date"]'
    publish_time_re = u'.*?(\d{4})-(\d{2})-(\d{2})\s+(\d{2}:\d{2}).*'
    publish_time_format = '%Y%m%d%H:%M'
    source_xpath = '//*[@class="media_name"]'

    site_domain = 'xcar.com.cn'
    site_name = u'爱卡汽车'
