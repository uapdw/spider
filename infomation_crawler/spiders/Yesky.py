# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule


from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
from scrapy.http import Request
import re


class Yesky(CrawlSpider):
  name = 'NEWSyesky'

  allowed_domains = ['news.yesky.com']
  start_urls = ['http://news.yesky.com/']
  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles
  rules = (
      Rule(SgmlLinkExtractor(allow=(r'http://news.yesky.com/\d+/\d+.shtml')),callback='parse_item'),
  )

  def parse_item(self, response):
    reHtml = re.compile('</?\w+[^>]*>')
    reP = re.compile('<\s*p[^>]*>[^<]*<\s*/\s*p\s*>',re.I)
    reA = re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>',re.I)
    abstract = []
    sel = Selector(response)
    i =WebArticleItem()
    title = sel.xpath('//h1/text()').extract()
    i['title'] = len(title)>0 and title[0].strip() or ''
    i['siteName'] = 'yesky'
    i['url'] = response.url
    author = sel.xpath('//div[@class="editor"]/span/text()').extract()
    i['author'] = len(author)>0 and author[0].split(u'\uff1a')[1].strip() or ''
    source = sel.xpath('//div[@class="detail"]/span[1]/text()').extract()
    i['source'] = len(source)>0 and source[0].strip() or ''
    pubtime = sel.xpath('//div[@class="detail"]/span[2]/text()').extract()
    i['publishTime'] = len(pubtime)>0 and pubtime[0].split(' ')[0] or str(datetime.date.today())
    i['addTime'] = datetime.datetime.now()
    content= sel.xpath('//div[@class="article"]').extract()
    detail = reP.sub('',content[0])
    detail = reA.sub('',detail)
    abstract.append(reHtml.sub('',detail))

    #i['addTime'] = (len(sel.xpath('//div[@class="detail"]/span[2]/text()').extract())) and sel.xpath('//div[@class="detail"]/span[2]/text()').extract()[0] or ''
    i['content'] = len(content)>0 and content[0] or ''
    i['keyWords'] = ''
    i['abstract'] = abstract[0][0:200].strip()
    return i






