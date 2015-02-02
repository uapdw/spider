# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule


from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
from scrapy.http import Request
import re
class ItbearSpider(CrawlSpider):
    name = 'ItbearSpider'
    allowed_domain = ['itbear.com.cn']
    start_urls= ['http://www.itbear.com.cn/scroll.aspx']
    conn = pymongo.Connection('localhost',27017)
    infoDB = conn.info
    tWebArticles = infoDB.web_articles
    #rules = [
    #   Rule(SgmlLinkExtractor(allow=(r'http://www.cctime.com/scroll/default.asp\?kpage=\d+'))),
    #   Rule(SgmlLinkExtractor(allow=(r'http://www.cctime.com/html/\d{4}-\d{2}-\d{2}/\d+.htm'),restrict_xpaths=('//td[@id="zList"]')),callback='parse_item'),
    #]

    def parse_item(self, response):

        sel = Selector(response)
        i = response.meta['item']
        i['siteName'] = 'itbear'
        title = sel.xpath('//h1/text()').extract()
        i['title'] = len(title)>0 and title[0].strip() or ''
        pubtime = sel.xpath('//div[@id="printBody"]/text()').re(r'\s?.*\d{4}-\d{2}-.*\s?.*')
        i['publishTime'] = len(pubtime)>0 and pubtime[0].split(u'\uff1a')[1].replace(u'\xa0',' ').split(' ')[0] or str(datetime.date.today())
        i['source'] = len(pubtime[0].split(u'\uff1a'))>2 and pubtime[0].split(u'\uff1a')[2].replace(u'\xa0',' ').split(' ')[0] or ''
        i['author'] = len(pubtime[0].split(u'\uff1a'))>3 and pubtime[0].split(u'\uff1a')[3].replace(u'\xa0',' ').split(' ')[0] or ''

        i['addTime'] = datetime.datetime.now()
        content = sel.xpath('//div[@id="content"]').extract()
        i['content'] = len(content)>0 and content[0] or ''
        i['abstract'] = ''
        return i
    def parse(self, response):
        sel = Selector(response)
        items = []
        url=sel.xpath('//div[@class="mframe mR"]//div[@class="wrapper"]//ul[@class="nl"]//li')[0:]
        for newsurl in url:
            i = WebArticleItem()
            url_temp = 'http://www.itbear.com.cn/' + newsurl.xpath('a[2]/@href').extract()[0]
            keywords = newsurl.xpath('a[1]/text()').extract()
            i['keyWords'] = len(keywords)>0 and keywords[0] or ''
            i['url'] = url_temp
            items.append(i)
        for item in items:
            yield Request(item['url'],meta={'item':item},callback=self.parse_item)








