# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import JXHrssNewsLoader


class JXHrssNewsSpider(LoaderMappingSpider):
    '''江西省人力资源和社会保障厅爬虫'''

    name = 'jxhrss_gov_cn_news' 
    allowed_domains = [ 'jxhrss.gov.cn', ]
    start_urls = ['http://www.jxhrss.gov.cn/']

    mapping = {
        'view.aspx\?TaskNo=\d+&ID=\d+': JXHrssNewsLoader
    }