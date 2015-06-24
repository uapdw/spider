from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
import re

class ChinaByteSpider(CrawlSpider):
  name = 'chinabyte'
  allowed_domains = ['chinabyte.com']
  start_urls = ['http://info.chinabyte.com/','http://cloud.chinabyte.com/']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'(info|cloud)\.chinabyte\.com/\d+/\d+\.shtml', deny=r'icloud\.chinabyte\.com'), callback='parse_item'),
  )

  def parse_item(self, response):
    print "enter chinabyte_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()
    
    title = sel.xpath('//h1/text()').extract()
    i['title'] = len(title)>0 and title[0].strip() or ''

    i['url'] = response.url

    pubTime = sel.xpath('//div[@class="info"]/span[@class="date"]/text()').extract()
    source = sel.xpath('//div[@class="info"]/span[@class="where"]/text()').extract()
    author = sel.xpath('//div[@class="info"]/span[@class="auth"]/text()').extract()
    i['publishTime'] = len(pubTime)>0 and pubTime[0].split()[0] or str(datetime.date.today())
    i['source'] = len(source)>0 and source[0] or ''
    i['author'] = len(author)>0 and author[0] or ''
    
    i['abstract'] = ''
    
    keyWordList = sel.xpath('//div[@class="keywords"]/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords

    content = sel.xpath('//div[@id="logincontent"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'chinabyte'

    i['addTime'] = datetime.datetime.now()

    return i
