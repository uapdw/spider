# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.jxys_org_cn.jxys_org_cn_news import (
    JxysOrgCnNewsLoader
)


class JxysOrgCnNewsSpider(LoaderMappingSpider):

    u"""江西有色金属信息网新闻爬虫"""

    name = 'jxys_org_cn_news'
    allowed_domains = ['jxys.org.cn']
    start_urls = ['http://www.jxys.org.cn/']

    mapping = {
        'jxys\.org\.cn/view\.asp\?NewsNo=\d+':
        JxysOrgCnNewsLoader
    }
