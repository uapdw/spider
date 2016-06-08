# -*- coding: utf-8 -*-

from spider.loader.loaders import NewsLoader

class SgccComCnNewsLoader(NewsLoader):

    u"""国家电网新闻"""

    title_xpath = '//*[@class="cSgcc"]'
    content_xpath = '//*[@class="blkContainerSblkCon_14"]'

    publish_time_xpath = '//*[@class="blkContainerSblkCon_14"]/div'
    publish_time_re = u'.*?发布时间：\s*(\d{4}-\d{2}-\d{2}).*'
    publish_time_format = '%Y-%m-%d'

    source_xpath = '//*[@class="blkContainerSblkCon_14"]'
    source_re = u'.*?信息来源：\s*(\S+).*'

    source_domain = 'sgcc.com.cn'
    source_name = u'国家电网'
