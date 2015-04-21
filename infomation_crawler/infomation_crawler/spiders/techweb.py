from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
import re

class TechwebSpider(CrawlSpider):
  name = 'techweb'
  allowed_domains = ['techweb.com.cn']
  start_urls = ['http://www.techweb.com.cn/news']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'www\.techweb\.com\.cn/\D+/\d{4}-\d{2}-\d{2}/\d+\.shtml'), callback='parse_item'),
  )

  def parse_item(self, response):
    print "enter techweb_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()

    title = sel.xpath('//div[@class="title"]/h1/text()').extract()
    i['title'] = len(title)>0 and title[0].strip() or ''

    i['url'] = response.url

    pubTime = sel.xpath('//div[@class="titleBar"]/span[@class="date"]/text()').extract()
    source = sel.xpath('//div[@class="titleBar"]/span[@class="where"]/a/text()').extract()
    author = sel.xpath('//div[@class="titleBar"]/span[@class="author"]/text()').extract()
    i['publishTime'] = len(pubTime)>0 and pubTime[0].split()[0].replace('.','-') or str(datetime.date.today())
    i['source'] = len(source)>0 and source[0].strip() or ''
    i['author'] = len(author)>0 and author[0].split(':')[1] or ''
    
    i['abstract'] = ''
    
    keyWordList = sel.xpath('//div[@class="tag-editor"]/span[@class="tag"]/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords

    content = sel.xpath('//div[@id="artibody"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'techweb'

    i['addTime'] = datetime.datetime.now()

    return i
