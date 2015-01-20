# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule


from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
from scrapy import Spider,Request
class YnetSpider(CrawlSpider):
    name = 'YnetSpider'
    allowed_domain = ['news.ynet.com']
    start_urls= ['http://news.ynet.com/']
    conn = pymongo.Connection('localhost',27017)
    infoDB = conn.info
    tWebArticles = infoDB.web_articles
    rules = (
       Rule(SgmlLinkExtractor(allow=r'news.ynet.com/3.1/\d{4}/\d{2}/\d+.html',deny=r'(6783557|8770813).html',restrict_xpaths=('//div[@class="HC Fir" or @class="HC world" or @class="hcc" or @class="hcr"]')),callback='parse_item'),
    )

    def parse_item(self, response):
        sel = Selector(response)
        i = WebArticleItem()
        i['siteName'] = 'ynet'
        title = sel.xpath('//h1/text()').extract()
        i['title'] = len(title)>0 and title[0].strip() or ''
        i['url'] = response.url
        pubtime=sel.xpath('//span[@id="pubtime_baidu"]/text()').re(r'\d{4}-\d{2}-\d{2}')
        i['publishTime'] = len(pubtime)>0 and pubtime[0] or str(datetime.date.today())
        i['addTime'] = datetime.datetime.now()
        #author = sel.xpath('//span[@id="author_baidu"]/text()').extract()
        i['author'] = ''
        source = sel.xpath('//p[@class="pd10 fs12"]/span[2]/text()').extract()
        i['source'] = len(source)>0 and source[0].split(u'\uff1a')[1].strip() or ''
        content = sel.xpath('//div[@id="pzoom"]').extract()
        i['content'] = len(content)>0 and content[0] or ''
        i['keyWords'] = ''
        i['abstract'] = ''
        return i


