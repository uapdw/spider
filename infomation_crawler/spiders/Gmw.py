# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule


from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
from scrapy import Spider,Request
import re

__author__ = 'Administrator'
class GmwSpider(CrawlSpider):
    name = 'GmwSpider'
    allowed_domain = ['gmw.cn']
    start_urls = ['http://news.gmw.cn/']
    conn = pymongo.Connection('localhost',27017)
    infoDB = conn.info
    tWebArticles = infoDB.web_articles
    #rules = [
    #    Rule(SgmlLinkExtractor(allow=r'http://.gmw.cn/\d{4}-\d{2}/\d+/content_\d+.htm'),callback='parse_item',follow=True)
    #]
    def parse_item(self, response):
        sel = Selector(response)
        i = response.meta['item']
        title = sel.xpath('//h1[@id="articleTitle"]/text()|//div[@id="articleTitle"]/text()').extract()
        i['title'] = len(title)>0 and title[0].strip() or ''
        source =sel.xpath('//div[@id="contentMsg"]/span[@id="source"]/text()').extract()
        i['source'] = len(source)>0 and source[0].split(u'\uff1a')[1].strip() or ''
        i['author'] = ''
        pubTime = sel.xpath('//div[@id="contentMsg"]/span[@id="pubTime"]/text()').extract()
        #i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
        i['publishTime'] = len(pubTime)>0 and pubTime[0].split(' ')[0] or str(datetime.date.today())
        i['keyWords'] = ''
        i['abstract'] = ''
        content = sel.xpath('//div[@id="contentMain"]').extract()
        i['content'] = len(content)>0 and content[0] or ''
        i['siteName'] = 'gmw'
        i['addTime'] = datetime.datetime.now()
        return i
    def parse(self, response):
        sel = Selector(response)
        items = []
        newurl = sel.xpath('//div[@class="box_mid"]/p/span/a|//div[@class="box_mid"]/p/a')[0:]
        #i = WebArticleItem1()
        for news in newurl:
            i = WebArticleItem()
            urltmp=news.xpath('@href').extract()[0]
            urllink=re.sub(r'^\d.*','http://news.gmw.cn/'+urltmp,urltmp)
            i['url'] = urllink
            items.append(i)
        for item in items:
                yield Request(item['url'],meta={'item':item},callback=self.parse_item)






