from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo
import string

class CtocioSpider(CrawlSpider):
  name = 'ctocio'
  allowed_domains = ['ctocio.com']
  start_urls = ['http://www.ctocio.com/category/cloud','http://www.ctocio.com/category/bigdata','http://www.ctocio.com/category/security','http://www.ctocio.com/category/hotnews','http://www.ctocio.com/category/ccnews']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    author = sel.xpath('//ul[@class="postinfo"]/li/a/text()').extract()
    i['author'] = len(author)>0 and author[0].strip() or ''
    
    content = sel.xpath('//div[@class="entrys"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'ctocio'

    i['source'] = ''
    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    print "enter ctocio_parse_item...."
  
    monthDic = {u'\u4E00\u6708':1,u'\u4E8C\u6708':2,u'\u4E09\u6708':3,u'\u56DB\u6708':4,u'\u4E94\u6708':5,u'\u516D\u6708':6,u'\u4E03\u6708':7,u'\u516B\u6708':8,u'\u4E5D\u6708':9,u'\u5341\u6708':10,u'\u5341\u4E00\u6708':11,u'\u5341\u4E8C\u6708':12}
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@class="post archived"]')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = news.xpath('h2/a/@href').extract()[0]
      
      title = news.xpath('h2/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      pubTime = news.xpath('ul[@class="postinfo"]/li[1]/text()').extract()
      if len(pubTime)>0:
        chMonth = pubTime[0].split(',')[1].split()[0]
        month = monthDic[chMonth]
        day = string.atoi(pubTime[0].split(',')[1].split()[1])
        year = string.atoi(pubTime[0].split(',')[2])
        publishTime = str(datetime.date(year,month,day))
        i['publishTime'] = publishTime
      else:
        i['publishTime'] = str(datetime.date.today())

      abstract = news.xpath('div[@class="entry"]/text()').extract()
      i['abstract'] = len(abstract)>1 and abstract[1].strip() or ''

      keyWordList = news.xpath('div[@class="tags"]/a/text()').extract()
      keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
      for key in range(len(keyWordList)-1):
        keyWords = keyWords + '|' + keyWordList[key+1].strip()
      i['keyWords'] = keyWords
    
      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
