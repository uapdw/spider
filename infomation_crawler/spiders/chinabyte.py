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

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'(info|cloud)\.chinabyte\.com/\d+/\d+\.shtml', deny=r'icloud\.chinabyte\.com'), callback='parse_item'),
  )

  def parse_item(self, response):
    print "enter chinabyte_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()
    i['siteName'] = 'chinabyte'
    i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
    i['url'] = response.url
    i['addTime'] = datetime.datetime.now()
    i['content'] = (len(sel.xpath('//div[@id="logincontent"]').extract())) and sel.xpath('//div[@id="logincontent"]').extract()[0] or ''
    pubTimeStr = (len(sel.xpath('//span[@id="pubtime_baidu"]/text()').extract())>0) and sel.xpath('//span[@id="pubtime_baidu"]/text()').extract()[0] or ''
    publishTime = re.findall(r'\d{4}-\d{2}-\d{2}', pubTimeStr, re.M)
    if len(publishTime)>0:
      i['publishTime'] = publishTime[0]
    else:
      i['publishTime'] = ''    
    tagWords = sel.xpath('//div[@class="keywords"]/a/text()').extract()
    keyWords = len(tagWords)>0 and tagWords[0].strip() or ''
    for m in range(len(tagWords)-1):
      keyWords = keyWords + '|' + tagWords[m+1].strip()
    i['keyWords'] = keyWords
    return i
