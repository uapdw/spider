# -*- coding: utf-8 -*-

from spider.spiders import LoaderMappingSpider
from spider.loader.loaders import DataTsciComCnNewsLoader


class DataTsciComCnNewsSpider(LoaderMappingSpider):

    u"""深度数据新闻爬虫"""

    name = 'data_tsci_com_cn_news'
    allowed_domains = ['data.tsci.com.cn']
    start_urls = ['http://data.tsci.com.cn/']

    mapping = {
        'data\.tsci\.com\.cn/News/HTM/\d{8}/\d+.htm': DataTsciComCnNewsLoader,
        'data\.tsci\.com\.cn/News/NewsShow\.aspx\?NewsId=\d+':
        DataTsciComCnNewsLoader
    }
