# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from spider.loader.loaders.baidu_com.baidu_com_news import BaiduNewsLoader
from urllib import quote

class BaiduNewsSpider(CrawlSpider):
    u"""百度新闻爬虫"""

    name = 'baidu_com_news'

    allowed_domains = ['baidu.com']

#     start_url_pattern = 'http://news.baidu.com/ns?cl=2&rn=20&tn=news&word=%s'
    start_url_pattern = 'http://news.baidu.com/ns?word=%s&pn=%s&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0'

    categories = [u'北汽', u'北汽B40', u'哈弗']
    
    def __init__(self):
        self.start_urls = []
        for category in self.categories:
            for pn in xrange(30):
                self.start_urls.append(self.start_url_pattern % (quote(category.encode('utf-8')), pn*20 ))

    def parse(self, response):
        l = BaiduNewsLoader()
        return l.load(response)
