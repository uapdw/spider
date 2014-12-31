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
class PcpopSpider(CrawlSpider):
    name = 'PcpopSpider'
    allowed_domain = ['pcpop.com']
    start_urls = ['http://news.pcpop.com/nb/PackageTmp/ReadTxt.ashx?r=5&channelId=23&propertyId=0&categoryId=005900050',
                  'http://news.pcpop.com/nb/PackageTmp/ReadTxt.ashx?r=7&channelId=23&propertyId=0&categoryId=000000228',
                  'http://news.pcpop.com/nb/PackageTmp/ReadTxt.ashx?r=50&channelId=23&propertyId=0&categoryId=005500045',
                  'http://news.pcpop.com/nb/PackageTmp/ReadTxt.ashx?r=54&channelId=23&propertyId=0&categoryId=000000242',
                  'http://news.pcpop.com/nb/PackageTmp/ReadTxt.ashx?r=23&channelId=23&propertyId=0&categoryId=005600046',
                  'http://news.pcpop.com/nb/PackageTmp/ReadTxt.ashx?r=40&channelId=23&propertyId=0&categoryId=006000053',
                  'http://news.pcpop.com/nb/PackageTmp/ReadTxt.ashx?r=57&channelId=23&propertyId=0&categoryId=005000080'
    ]
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
        source =sel.xpath('//div[@class="chuchu"]/a/text()').extract()
        i['source'] = len(source)>0 and source[0] or ''
        pubTime = sel.xpath('//span[@id="pubtime_baidu"]/text()').extract()
        #i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
        content = sel.xpath('//div[@class="main"]').extract()
        i['content'] = len(content)>0 and content[0] or ''
        i['siteName'] = 'pcpop.com'
        i['addTime'] = datetime.datetime.now()
        return i
    def parse(self, response):
        sel = Selector(response)
        items = []
        newurl = sel.xpath('//div[@class="left_cont2_2"]')[0:]
        #i = WebArticleItem1()
        re_h = re.compile(r'[\[|\]]')
        for news in newurl:
            i = WebArticleItem()
            urllink=news.xpath('div[@class="left_tit2"]/a/@href').extract()[0]
            #urllink=re.sub(r'^\d.*','http://news.gmw.cn/'+urltmp,urltmp)
            i['url'] = urllink
            pubTime = news.xpath('div[@class="left_message1"]/text()').re(r'\d{4}-\d{2}-\d{2}')
            i['publishTime'] = len(pubTime)>0 and pubTime[0] or str(datetime.date.today())
            author = news.xpath('div[@class="left_message1"]/text()').extract()
            i['author'] = len(author)>0 and author[0].strip().split(' ')[0].split(u'\uff1a')[1] or ''
            keyWordList = news.xpath('div[@class="left_message1"]/span/a/text()').extract()
            keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
            for key in range(len(keyWordList)-1):
                keyWords = keyWords + '|' + keyWordList[key+1].strip()
            i['keyWords'] = keyWords
            abstract = news.xpath('div[@class="left_cont2_3"]/div[@class="left_wordcon1"]/text()').extract()
            i['abstract'] = len(abstract)>0 and abstract[0] or ''
            items.append(i)
        for item in items:
                yield Request(item['url'],meta={'item':item},callback=self.parse_item)






