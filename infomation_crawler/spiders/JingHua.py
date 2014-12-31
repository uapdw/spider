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
class JingHSpider(CrawlSpider):
    name = 'JingHSpider'
    allowed_domain = ['jinghua.cn']
    start_urls = ['http://news.jinghua.cn/']
    conn = pymongo.Connection('localhost',27017)
    infoDB = conn.info
    tWebArticles = infoDB.web_articles
    #rules = [
    #    Rule(SgmlLinkExtractor(allow=r'http://.gmw.cn/\d{4}-\d{2}/\d+/content_\d+.htm'),callback='parse_item',follow=True)
    #]
    def parse_item(self, response):
        sel = Selector(response)
        i = response.meta['item']
        title = sel.xpath('//h1/text()').extract()
        i['title'] = len(title)>0 and title[0].replace(u'\xa0',' ') or ''
        source =sel.xpath('//span[@id="source_baidu"]/a/text()').extract()
        i['source'] = len(source)>0 and source[0] or ''
        i['author'] = ''
        pubTime = sel.xpath('//span[@id="pubtime_baidu"]/text()').extract()
        #i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
        i['publishTime'] = len(pubTime)>0 and pubTime[0].split(' ')[0] or str(datetime.date.today())
        content = sel.xpath('//div[@class="ncwrap"]').extract()
        i['content'] = len(content)>0 and content[0] or ''
        i['siteName'] = 'jinghua'
        i['addTime'] = datetime.datetime.now()
        return i
    def parse(self, response):
        sel = Selector(response)
        items = []
        newurl = sel.xpath('//div[@class="list"]//dl')[0:]
        #i = WebArticleItem1()
        re_h = re.compile(r'[\[|\]]')
        for news in newurl:
            i = WebArticleItem()
            urllink=news.xpath('dt/a/@href').extract()[0]
            #urllink=re.sub(r'^\d.*','http://news.gmw.cn/'+urltmp,urltmp)
            i['url'] = urllink
            keywords = news.xpath('dt/text()').extract()[0]
            i['keyWords'] = len(keywords)>0 and re_h.sub('',keywords).strip() or ''
            abstract = news.xpath('dd/text()').extract()[0]
            i['abstract'] = len(abstract)>0 and abstract or ''
            items.append(i)
        for item in items:
                yield Request(item['url'],meta={'item':item},callback=self.parse_item)






