# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import JXFNewsLoader


class JXFNewsSpider(LoaderMappingSpider):
    '''江西省财政厅爬虫'''

    name = 'jxf_gov_cn_news' 
    allowed_domains = [ 'jxf.gov.cn', ]
    start_urls = ['http://www.jxf.gov.cn/']

    mapping = {
        'JxfShowViews_pid_.*.shtml': JXFNewsLoader
    }