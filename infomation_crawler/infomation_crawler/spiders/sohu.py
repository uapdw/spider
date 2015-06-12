from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
import re

class SohuSpider(CrawlSpider):
  name = 'sohu'
  allowed_domains = ['sohu.com']
  start_urls = ['http://it.sohu.com/']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'(it|digi)\.sohu\.com/\d{8}'), callback='parse_item'),
  )

  def parse_item(self, response):
    print "enter sohu_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()
    
    title = sel.xpath('//h1[@itemprop="headline"]/text()').extract()
    i['title'] = len(title)>0 and title[0].strip() or ''

    i['url'] = response.url

    pubTime = sel.xpath('//div[@class="time-source"]/div[@class="time"]/text()').extract()
    pubTime = len(pubTime)>0 and pubTime or sel.xpath('//div[@class="news-info"]/span[@class="time"]/text()').extract()
    source = sel.xpath('//div[@class="time-source"]/div[@class="source"]/span[1]/span/span/text()').extract()
    source = len(source)>0 and source or sel.xpath('//div[@class="news-info"]/span[@class="source"]/span[1]/span/span/text()').extract()
    author = sel.xpath('//div[@class="time-source"]/div[@class="source"]/span[2]/text()').extract()
    author = len(author)>0 and author or sel.xpath('//div[@class="news-info"]/span[@class="source"]/span[2]/text()').extract()
    i['publishTime'] = len(pubTime)>0 and pubTime[0].split()[0] or str(datetime.date.today())
    i['source'] = len(source)>0 and source[0].strip() or ''
    i['author'] = len(author)>0 and author[0].strip().replace(u'\u4f5c\u8005\uff1a','') or ''
    
    i['abstract'] = ''
    i['keyWords'] = ''

    content = sel.xpath('//div[@itemprop="articleBody"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'sohu'

    i['addTime'] = datetime.datetime.now()

    return i
