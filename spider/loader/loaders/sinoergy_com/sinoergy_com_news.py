# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class SinoergyComNewsLoader(NewsLoader):

    u"""华夏能源网新闻"""

    title_xpath = '//*[@class="clearfix neirong"]/h1'
    content_xpath = '//*[@class="neirong-box"]'

    author_xpath = '//*[@class="recommenders"]/a'

    publish_time_xpath = '//*[@class="neirong-other"]/time'
    publish_time_re = u'.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*'
    publish_time_format = '%Y-%m-%d %H:%M'

    source_domain = 'sinoergy.com'
    source_name = u'华夏能源网'
