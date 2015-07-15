from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class LeiphoneSpider(CrawlSpider):
  name = 'leiphone'
  allowed_domains = ['leiphone.com']
  start_urls = ['http://www.leiphone.com/tag/%E5%A4%A7%E6%95%B0%E6%8D%AE']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  def __init__(self,**kw):
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)


  def __del__(self):
    self.transport.close()

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    author = sel.xpath('//div[@class="pi-author"]/a/text()').extract()
    i['author'] = len(author)>0 and author[0].strip() or ''

    pubTime = sel.xpath('//div[@class="pi-author"]/span/text()').extract()
    i['publishTime'] = len(pubTime)>0 and pubTime[0].strip() or str(datetime.date.today())
    
    content = sel.xpath('//div[@class="pageCont lp-article-comView "]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'leiphone'

    i['source'] = ''
    i['addTime'] = datetime.datetime.now()

    keyWordList = sel.xpath('//div[@class="pageTag"]/ul/li/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords
    
    return i

  def parse(self, response):
    print "enter leiphone_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//article[@class="lp-articles"]/div[@class="article-top clr"]/div[@class="article-right"]')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = news.xpath('h2/a/@href').extract()[0]
      
      title = news.xpath('h2/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      abstract = news.xpath('div[@class="article-right-text"]/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0] or ''

      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
