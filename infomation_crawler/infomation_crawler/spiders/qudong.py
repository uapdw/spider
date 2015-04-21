# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule


from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
from scrapy.http import Request
import re
class QuDongSpider(CrawlSpider):
    name = 'qudong'
    allowed_domain = ['qudong.com']
    start_urls= ['http://news.qudong.com/']
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
        i['siteName'] = 'qudong'
        title = sel.xpath('//h1/text()').extract()
        i['title'] = len(title)>0 and title[0].strip() or ''
        pubtime = sel.xpath('//div[@class="article-infos"]/span[@class="date"]/text()').re(r'\d{4}-\d{2}-\d{2}')
        i['publishTime'] = len(pubtime)>0 and pubtime[0].strip() or str(datetime.date.today())
        source = sel.xpath('//div[@class="article-infos"]/span[@class="source"]/a/text()').extract()
        i['source'] = len(source)>0 and source[0].strip() or ''
        author = sel.xpath('//div[@class="article-infos"]/span[@class="editors"]/a/text()').extract()
        i['author'] = len(author)>0 and author[0].strip() or ''

        i['addTime'] = datetime.datetime.now()
        content = sel.xpath('//div[@class="article-content fontSizeSmall BSHARE_POP"]').extract()
        i['content'] = len(content)>0 and content[0] or ''

        return i
    def parse(self, response):
        sel = Selector(response)
        items = []
        url=sel.xpath('//div[@class="lxfeng"]/div[@class="clearfix"]/div[@class="hot-text"]')[0:]
        for newsurl in url:
            i = WebArticleItem()
            url_temp = newsurl.xpath('h2/a/@href').extract()[0]
            keywordList = newsurl.xpath('span[2]/a/text()').extract()
            keywords = len(keywordList)>0 and keywordList[0].strip() or ''
            for keyword in range(len(keywordList)-1):
                keywords = keywords + '|' + keywordList[keyword+1].strip()
            i['keyWords'] = keywords
            i['abstract'] = newsurl.xpath('p/a/text()').extract()[0]
            i['url'] = url_temp
            items.append(i)
        for item in items:
            yield Request(item['url'],meta={'item':item},callback=self.parse_item)








