from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
import re

class tech163Spider(CrawlSpider):
  name = 'tech163'
  allowed_domains = ['163.com']
  start_urls = ['http://tech.163.com/']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'tech\.163\.com/\d{2}/\d{4}'), callback='parse_item'),
  )

  def parse_item(self, response):
    print "enter tech163_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()
    
    title = sel.xpath('//h1[@id="h1title"]/text()').extract()
    i['title'] = len(title)>0 and title[0].strip() or ''

    i['url'] = response.url

    pubTime = sel.xpath('//div[@class="ep-time-soure cDGray"]/text()').extract()
    pubTime = len(pubTime)>0 and pubTime or sel.xpath('//div[@class="ep-info cDGray"]/div/text()').extract()
    print pubTime
    i['publishTime'] = len(pubTime)>0 and pubTime[0].split()[0] or str(datetime.date.today())
    source = sel.xpath('//div[@class="ep-time-soure cDGray"]/a/text()').extract()
    source = len(source)>0 and source or sel.xpath('//div[@class="ep-info cDGray"]/div/a/text()').extract()
    i['source'] = len(source)>0 and source[0] or ''

    i['author'] = ''
    i['abstract'] = ''
    i['keyWords'] = ''

    content = sel.xpath('//div[@id="endText"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'tech.163'

    i['addTime'] = datetime.datetime.now()

    return i
