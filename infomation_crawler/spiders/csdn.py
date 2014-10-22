from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo
import re

class CsdnSpider(CrawlSpider):
  name = 'csdn'
  allowed_domains = ['csdn.net']
  start_urls = ['http://www.csdn.net/tag/%E5%A4%A7%E6%95%B0%E6%8D%AE/news', 'http://www.csdn.net/tag/%E5%AE%89%E5%85%A8/news', 'http://www.csdn.net/tag/%E7%A7%BB%E5%8A%A8/news', 'http://www.csdn.net/tag/%E4%BA%91%E8%AE%A1%E7%AE%97/news', 'http://www.csdn.net/tag/%E9%9B%86%E6%88%90/news', 'http://www.csdn.net/tag/%E5%95%86%E4%B8%9A%E5%88%86%E6%9E%90/news', 'http://www.csdn.net/tag/%E5%BC%80%E5%8F%91%E5%B9%B3%E5%8F%B0/news']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles
  
  #yesterday = datetime.date.today() - datetime.timedelta(days=1)
  today = datetime.date.today()  

  rules = (
    Rule(SgmlLinkExtractor(allow=r'/article/(.*)'+str(today)), callback='parse_item'),
  )

  def parse_item(self, response):
    print "enter Csdn_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()
    i['siteName'] = 'csdn'
    i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
    i['url'] = response.url
    i['addTime'] = datetime.datetime.now()
    i['content'] = (len(sel.xpath('//div[@class="con news_content"]').extract())) and sel.xpath('//div[@class="con news_content"]').extract()[0] or ''
    publishTime = re.findall(r'\d{4}-\d{2}-\d{2}', response.url, re.M)
    if len(publishTime)>0:
      i['publishTime'] = publishTime[0]
    else:
      i['publishTime'] = ''
    tagWords = sel.xpath('//div[@class="tag"]/a/text()').extract()
    keyWords = tagWords[0].strip()
    for m in range(len(tagWords)-1):
      keyWords = keyWords + '|' + tagWords[m+1].strip()
    i['keyWords'] = keyWords
    return i

