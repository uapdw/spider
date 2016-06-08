# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders.newenergy_org_cn.newenergy_org_cn_news import(
    NewenergyOrgCnNewsLoader
)


class NewenergyOrgCnNewsSpider(LoaderMappingSpider):

    u"""中国新能源网新闻爬虫"""

    name = 'newenergy_org_cn_news'
    allowed_domains = ['newenergy.org.cn']
    start_urls = ['http://www.newenergy.org.cn/']

    mapping = {
        'www.newenergy.org.cn/\S+/\S+/\d{6}/t\d{8}_\d+.html' or
        'www.newenergy.org.cn/\S+/\d{6}/t\d{8}_\d+.html':
        NewenergyOrgCnNewsLoader
    }
