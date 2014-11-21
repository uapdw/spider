from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo

class It168Spider(CrawlSpider):
  name = 'it168'
  allowed_domains = ['it168.com']
  
  today = datetime.date.today()
  year = today.year
  yesterday = today - datetime.timedelta(days=1)

  safeURL = 'http://archive.it168.com/100002/' + str(year) + '/' + str(yesterday) + '.shtml'
  cloudURL = 'http://archive.it168.com/100043/' + str(year) + '/' + str(yesterday) + '.shtml'
  urls = []
  urls.append(safeURL)
  urls.append(cloudURL)
  start_urls = urls

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    author = sel.xpath('//div[@class="cen01"]/text()').extract()
    i['author'] = len(author)>1 and author[1].split()[1][3:] or ''

    i['abstract'] = ''
    
    keyWordList = sel.xpath('//div[@class="biaoq"]/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords  

    content = sel.xpath('//div[@id="detailWord"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'it168'
    i['source'] = ''
    i['addTime'] = datetime.datetime.now()

    return i    

  def parse(self, response):
    print "enter it168_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@class="notebook_list"]/ul/li')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = news.xpath('a/@href').extract()[0]

      title = news.xpath('a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''

      pubTime = news.xpath('span/text()').extract()
      i['publishTime'] = len(pubTime)>0 and pubTime[0].strip()[1:-1] or str(It168Spider.yesterday)
      
      items.append(i)
    
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
